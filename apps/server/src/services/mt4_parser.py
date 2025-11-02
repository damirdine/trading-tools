from bs4 import BeautifulSoup
from datetime import datetime
import os

def parse_trade_data(file_path):
    """
    Parse MT4 HTML export file and extract trade data including all transactions.
    
    Args:
        file_path: Path to the MT4 .htm export file
        
    Returns:
        List of transaction dictionaries including trades, deposits, withdrawals, and balance changes
    """
    transaction_data = []
    
    if not os.path.exists(file_path):
        print(f"File not found: {file_path}")
        return transaction_data
    
    print(f"Parsing MT4 file: {file_path}")
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            soup = BeautifulSoup(file.read(), 'html.parser')
            
        # Find the table containing trade data
        tables = soup.find_all('table')
        if not tables:
            return transaction_data
        
        # Typically MT4 exports have trade data in the second table
        trade_table = tables[-1] if len(tables) > 1 else tables[0]
        rows = trade_table.find_all('tr')
        
        # Skip header rows
        for row in rows[1:]:
            cols = row.find_all('td')
            if len(cols) < 2:  # Skip empty rows
                continue
            
            try:
                transaction_type = cols[2].text.strip() if len(cols) > 2 else ''
                
                # Handle balance/deposit/withdrawal transactions
                if transaction_type == 'balance':
                    try:
                        balance_amount = float(cols[-1].text.strip().replace(',', ''))
                        transaction_entry = {
                            'ticket': cols[0].text.strip(),
                            'date': cols[1].text.strip(),
                            'type': 'balance',
                            'description': cols[3].text.strip() if len(cols) > 3 else '',
                            'amount': balance_amount,
                            'symbol': '',
                            'size': 0,
                            'open_price': 0,
                            'close_price': 0,
                            'profit': balance_amount
                        }
                        transaction_data.append(transaction_entry)
                    except (ValueError, IndexError):
                        continue
                
                # Handle regular trades (buy/sell)
                elif transaction_type.lower() in ['buy', 'sell'] and len(cols) >= 10:
                    try:
                        trade_entry = {
                            'ticket': cols[0].text.strip(),
                            'open_time': cols[1].text.strip(),
                            'type': transaction_type,
                            'size': float(cols[3].text.strip().replace(',', '')),
                            'symbol': cols[4].text.strip(),
                            'open_price': float(cols[5].text.strip().replace(',', '')),
                            'stop_loss': float(cols[6].text.strip().replace(',', '')) if cols[6].text.strip() else 0,
                            'take_profit': float(cols[7].text.strip().replace(',', '')) if cols[7].text.strip() else 0,
                            'close_time': cols[8].text.strip(),
                            'close_price': float(cols[9].text.strip().replace(',', '')) if cols[9].text.strip() else 0,
                        }
                        
                        # Commission is in column 10 (index 10)
                        if len(cols) > 10:
                            trade_entry['commission'] = float(cols[10].text.strip().replace(',', '')) if cols[10].text.strip() else 0
                        else:
                            trade_entry['commission'] = 0
                        
                        # Taxes in column 11 (index 11)
                        if len(cols) > 11:
                            trade_entry['taxes'] = float(cols[11].text.strip().replace(',', '')) if cols[11].text.strip() else 0
                        else:
                            trade_entry['taxes'] = 0
                        
                        # Swap in column 12 (index 12)
                        if len(cols) > 12:
                            trade_entry['swap'] = float(cols[12].text.strip().replace(',', '')) if cols[12].text.strip() else 0
                        else:
                            trade_entry['swap'] = 0
                        
                        # Profit is in column 13 (index 13)
                        if len(cols) > 13:
                            trade_entry['profit'] = float(cols[13].text.strip().replace(',', ''))
                        else:
                            trade_entry['profit'] = 0
                        
                        transaction_data.append(trade_entry)
                    except (ValueError, IndexError):
                        continue
            
            except Exception:
                continue
    
    except Exception as e:
        print(f"Error parsing MT4 file: {e}")
    
    return transaction_data



def parse_mt4_file(file_path):
    """
    Alias for parse_trade_data for backward compatibility.
    """
    return parse_trade_data(file_path)

def extract_trade_info(trade_data):
    """
    Extract summary information from trade data.
    
    Args:
        trade_data: List of transaction dictionaries (trades and balance entries)
        
    Returns:
        Dictionary with summary statistics including fees, PnL, deposits, and withdrawals
    """
    if not trade_data:
        return {
            'total_pnl': 0,
            'total_fees': 0,
            'total_deposits': 0,
            'total_withdrawals': 0,
            'total_volume': 0,
            'trade_count': 0,
            'winning_trades': 0,
            'losing_trades': 0,
            'win_rate': 0,
            'balance_transactions': 0
        }
    
    # Separate trades from balance transactions
    trades = [t for t in trade_data if t.get('type') in ['buy', 'sell']]
    balance_transactions = [t for t in trade_data if t.get('type') == 'balance']
    
    # Calculate PnL (Profit and Loss) from trades only
    total_pnl = sum(t.get('profit', 0) for t in trades)
    
    # Calculate total volume
    total_volume = sum(t.get('size', 0) for t in trades)
    
    # Count trades
    trade_count = len(trades)
    winning_trades = len([t for t in trades if t.get('profit', 0) > 0])
    losing_trades = len([t for t in trades if t.get('profit', 0) < 0])
    win_rate = (winning_trades / trade_count * 100) if trade_count > 0 else 0
    
    # Calculate deposits and withdrawals from balance entries
    total_deposits = sum(t.get('amount', 0) for t in balance_transactions if t.get('amount', 0) > 0 and 'Administration Fee' not in t.get('description', ''))
    total_withdrawals = sum(abs(t.get('amount', 0)) for t in balance_transactions if t.get('amount', 0) < 0 and 'Administration Fee' not in t.get('description', ''))
    
    # Calculate fees from both trade commissions and administration fees
    trade_commissions = sum(t.get('commission', 0) for t in trades if 'commission' in t)
    admin_fees = sum(abs(t.get('amount', 0)) for t in balance_transactions if 'Administration Fee' in t.get('description', '') and t.get('amount', 0) < 0)
    total_fees = trade_commissions + admin_fees
    
    return {
        'total_pnl': round(total_pnl, 2),
        'total_fees': round(total_fees, 2),
        'total_deposits': round(total_deposits, 2),
        'total_withdrawals': round(total_withdrawals, 2),
        'total_volume': round(total_volume, 2),
        'trade_count': trade_count,
        'winning_trades': winning_trades,
        'losing_trades': losing_trades,
        'win_rate': round(win_rate, 2),
        'balance_transactions': len(balance_transactions)
    }
    
    
    
if __name__ == "__main__":
    # Example usage
    current = os.getcwd()
    print(f"Current working directory: {current}")

    file = os.path.join(current, "data", "trade_data.htm")
    
    print(f"Using MT4 file path: {file}")

    mt4_file = file
    trades = parse_trade_data(mt4_file)
    import json
    json_data = json.dumps(trades, indent=4)
    with open("parsed_trades.json", "w", encoding="utf-8") as json_file:
        json_file.write(json_data)
    
    summary = extract_trade_info(trades)
    print(summary)