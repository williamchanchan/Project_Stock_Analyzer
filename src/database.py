import psycopg2
from config.settings import DATABASE_URL

def upsert_stock_data(df):
    """Inserts or updates stock price rows in PostgreSQL."""
    if df.empty:
        return
    
    conn = psycopg2.connect(DATABASE_URL)
    cursor = conn.cursor()
    
    insert_query = """
        INSERT INTO stock_prices (ticker, date, open, high, low, close, volume)
        VALUES (%s, %s, %s, %s, %s, %s, %s)
        ON CONFLICT (ticker, date) 
        DO UPDATE SET 
            open = EXCLUDED.open,
            high = EXCLUDED.high,
            low = EXCLUDED.low,
            close = EXCLUDED.close,
            volume = EXCLUDED.volume;
    """
    
    records = [tuple(row) for row in df.to_numpy()]
    
    try:
        cursor.executemany(insert_query, records)
        conn.commit()
        print(f"Successfully upserted {len(records)} records.")
    except Exception as e:
        conn.rollback()
        print(f"Database error: {e}")
    finally:
        cursor.close()
        conn.close()