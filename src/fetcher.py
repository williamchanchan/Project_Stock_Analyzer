import yfinance as yf
import pandas as pd

def fetch_latest_stock_data(ticker: str, period="5d") -> pd.DataFrame:
    """Fetches recent daily OHLCV data for a given ticker."""
    stock = yf.Ticker(ticker)
    df = stock.history(period=period)
    
    if df.empty:
        return pd.DataFrame()
    
    # Clean and format dataframe to match PostgreSQL table schema
    df = df.reset_index()
    df['Date'] = pd.to_datetime(df['Date']).dt.date
    
    clean_df = pd.DataFrame({
        'ticker': ticker,
        'date': df['Date'],
        'open': df['Open'],
        'high': df['High'],
        'low': df['Low'],
        'close': df['Close'],
        'volume': df['Volume']
    })
    
    return clean_df.dropna()