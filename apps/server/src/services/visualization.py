from typing import List, Dict, Optional
import matplotlib.pyplot as plt
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
import os

def generate_visualizations(analysis_data: Dict, period: str = "monthly") -> Dict:
    """
    Generate visualizations for trade data analysis.
    
    Args:
        analysis_data: Dictionary containing analyzed trade data
        period: Time period for analysis ('yearly', 'monthly', 'weekly', 'daily')
        
    Returns:
        Dictionary with visualization HTML and data
    """
    visualizations = {}
    
    try:
        # Create interactive Plotly charts
        if isinstance(analysis_data, list) and len(analysis_data) > 0:
            df = pd.DataFrame(analysis_data)
            
            # Profit over time chart
            if 'profit' in df.columns:
                fig = go.Figure()
                fig.add_trace(go.Scatter(
                    x=df.index,
                    y=df['profit'],
                    mode='lines+markers',
                    name='Profit'
                ))
                fig.update_layout(
                    title=f'{period.capitalize()} Profit Chart',
                    xaxis_title='Period',
                    yaxis_title='Profit',
                    hovermode='x unified'
                )
                visualizations['profit_chart'] = fig.to_html(div_id="profit_chart")
        
        visualizations['success'] = True
    except Exception as e:
        print(f"Error generating visualizations: {e}")
        visualizations['success'] = False
        visualizations['error'] = str(e)
    
    return visualizations

def generate_yearly_visualization(data: pd.DataFrame) -> str:
    yearly_data = data.resample('Y').sum()
    plt.figure(figsize=(10, 6))
    plt.plot(yearly_data.index, yearly_data['profit'], marker='o')
    plt.title('Yearly Profit Visualization')
    plt.xlabel('Year')
    plt.ylabel('Profit')
    plt.grid()
    plt.savefig('static/charts/yearly_profit.png')
    plt.close()
    return 'static/charts/yearly_profit.png'

def generate_monthly_visualization(data: pd.DataFrame) -> str:
    monthly_data = data.resample('M').sum()
    plt.figure(figsize=(10, 6))
    plt.bar(monthly_data.index, monthly_data['profit'], color='skyblue')
    plt.title('Monthly Profit Visualization')
    plt.xlabel('Month')
    plt.ylabel('Profit')
    plt.xticks(rotation=45)
    plt.grid()
    plt.savefig('static/charts/monthly_profit.png')
    plt.close()
    return 'static/charts/monthly_profit.png'

def generate_weekly_visualization(data: pd.DataFrame) -> str:
    weekly_data = data.resample('W').sum()
    plt.figure(figsize=(10, 6))
    plt.plot(weekly_data.index, weekly_data['profit'], marker='x', color='orange')
    plt.title('Weekly Profit Visualization')
    plt.xlabel('Week')
    plt.ylabel('Profit')
    plt.grid()
    plt.savefig('static/charts/weekly_profit.png')
    plt.close()
    return 'static/charts/weekly_profit.png'

def generate_daily_visualization(data: pd.DataFrame) -> str:
    daily_data = data.resample('D').sum()
    plt.figure(figsize=(10, 6))
    plt.plot(daily_data.index, daily_data['profit'], marker='s', color='green')
    plt.title('Daily Profit Visualization')
    plt.xlabel('Day')
    plt.ylabel('Profit')
    plt.grid()
    plt.savefig('static/charts/daily_profit.png')
    plt.close()
    return 'static/charts/daily_profit.png'

def clear_old_charts():
    chart_directory = 'static/charts/'
    for filename in os.listdir(chart_directory):
        file_path = os.path.join(chart_directory, filename)
        if os.path.isfile(file_path):
            os.remove(file_path)