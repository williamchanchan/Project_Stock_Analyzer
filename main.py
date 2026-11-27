from config.settings import WATCH_LIST
from src.fetcher import fetch_latest_stock_data
from src.database import upsert_stock_data
from src.analyzer import calculate_volume_oscillator, scan_for_opportunities
import pandas as pd
import psycopg2
from config.settings import DATABASE_URL

def load_full_history_from_db(ticker: str) -> pd.DataFrame:
    """Loads historical data from DB to compute rolling indicators accurately."""
    conn = psycopg2.connect(DATABASE_URL)
    query = "SELECT ticker, date, open, high, low, close, volume FROM stock_prices WHERE ticker = %s ORDER BY date ASC;"
    df = pd.read_sql(query, conn, params=(ticker,))
    conn.close()
    return df

def main():
    print("Starting daily stock update and scan...")
    for ticker in WATCH_LIST:
        print(f"Processing {ticker}...")
        
        # 1. Fetch latest data (e.g., last 5 days to catch any gaps)
        new_data = fetch_latest_stock_data(ticker, period="5d")
        if not new_data.empty:
            # 2. Update Database
            upsert_stock_data(new_data)
            
        # 3. Load full historical dataset from DB for indicator calculations
        full_df = load_full_history_from_db(ticker)
        if not full_df.empty and len(full_df) > 30:
            # 4. Run Technical Analysis
            analyzed_df = calculate_volume_oscillator(full_df)
            
            # 5. Check Opportunities
            scan_for_opportunities(analyzed_df, ticker)

    print("Execution complete.")

if __name__ == "__main__":
    main()