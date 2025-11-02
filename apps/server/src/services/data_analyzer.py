from datetime import datetime, timedelta
from typing import List, Dict
import pandas as pd

def analyze_trade_data(trade_data: List[Dict], period: str = "monthly") -> Dict:
    """
    Analyze trade data for a specified period.
    
    Args:
        trade_data: List of trade dictionaries
        period: Time period for analysis ('yearly', 'monthly', 'weekly', 'daily')
        
    Returns:
        Dictionary with analysis results
    """
    if not trade_data:
        return {
            'total_profit': 0,
            'total_volume': 0,
            'trades': [],
            'period': period
        }
    
    try:
        df = pd.DataFrame(trade_data)
        
        # Parse date columns
        date_column = 'open_time'
        if date_column in df.columns:
            df['date'] = pd.to_datetime(df[date_column], errors='coerce')
        else:
            df['date'] = pd.to_datetime(datetime.now())
        
        # Group by period
        if period == 'yearly':
            grouped = df.groupby(df['date'].dt.to_period('Y'))
        elif period == 'monthly':
            grouped = df.groupby(df['date'].dt.to_period('M'))
        elif period == 'weekly':
            grouped = df.groupby(df['date'].dt.to_period('W'))
        elif period == 'daily':
            grouped = df.groupby(df['date'].dt.to_period('D'))
        else:
            grouped = df.groupby(df['date'].dt.to_period('M'))
        
        results = []
        for period_key, group in grouped:
            result = {
                'period': str(period_key),
                'profit': group['profit'].sum() if 'profit' in group.columns else 0,
                'volume': group['size'].sum() if 'size' in group.columns else 0,
                'trades': len(group),
                'wins': len(group[group['profit'] > 0]) if 'profit' in group.columns else 0,
                'losses': len(group[group['profit'] < 0]) if 'profit' in group.columns else 0,
            }
            results.append(result)
        
        return {
            'total_profit': df['profit'].sum() if 'profit' in df.columns else 0,
            'total_volume': df['size'].sum() if 'size' in df.columns else 0,
            'total_trades': len(df),
            'results': results,
            'period': period
        }
    except Exception as e:
        print(f"Error analyzing trade data: {e}")
        return {
            'total_profit': 0,
            'total_volume': 0,
            'trades': [],
            'period': period,
            'error': str(e)
        }

def analyze_yearly(df: pd.DataFrame) -> Dict:
    """Analyze data by year."""
    df['date'] = pd.to_datetime(df['date'])
    return df.groupby(df['date'].dt.to_period('Y')).sum().to_dict(orient='records')

def analyze_monthly(df: pd.DataFrame) -> Dict:
    """Analyze data by month."""
    df['date'] = pd.to_datetime(df['date'])
    return df.groupby(df['date'].dt.to_period('M')).sum().to_dict(orient='records')

def analyze_weekly(df: pd.DataFrame) -> Dict:
    """Analyze data by week."""
    df['date'] = pd.to_datetime(df['date'])
    return df.groupby(df['date'].dt.to_period('W')).sum().to_dict(orient='records')

def analyze_daily(df: pd.DataFrame) -> Dict:
    """Analyze data by day."""
    df['date'] = pd.to_datetime(df['date'])
    return df.groupby(df['date'].dt.to_period('D')).sum().to_dict(orient='records')

def get_last_n_months_data(trade_data: List[Dict], months: int) -> List[Dict]:
    """
    Filter trade data to only include the last N months.
    
    Args:
        trade_data: List of trade dictionaries
        months: Number of months to include
        
    Returns:
        Filtered list of trades
    """
    cutoff_date = datetime.now() - timedelta(days=months * 30)
    return [trade for trade in trade_data 
            if pd.to_datetime(trade.get('open_time', datetime.now()), errors='coerce') >= cutoff_date]