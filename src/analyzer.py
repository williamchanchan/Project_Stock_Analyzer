import pandas as pd

def calculate_volume_oscillator(df: pd.DataFrame, short_window=14, long_window=28) -> pd.DataFrame:
    """Calculates the Volume Oscillator based on Volume EMAs."""
    df = df.sort_values('date').copy()
    
    # Calculate Short and Long EMAs of Volume
    ema_short = df['volume'].ewm(span=short_window, adjust=False).mean()
    ema_long = df['volume'].ewm(span=long_window, adjust=False).mean()
    
    # Volume Oscillator (% difference)
    df['vol_oscillator'] = ((ema_short - ema_long) / ema_long) * 1001
    
    return df

def scan_for_opportunities(df: pd.DataFrame, ticker: str):
    """Example strategy rule: Volume Oscillator crosses above a threshold or spikes."""
    if len(df) < 2:
        return False
    
    latest = df.iloc[-1]
    prev = df.iloc[-2]
    
    # Example condition: Volume Oscillator turns positive or spikes above 10%
    if latest['vol_oscillator'] > 10.0 and prev['vol_oscillator'] <= 10.0:
        print(f"[OPPORTUNITY] {ticker}: Volume Oscillator spiked to {latest['vol_oscillator']:.2f}% on {latest['date']}")
        return True
    return False