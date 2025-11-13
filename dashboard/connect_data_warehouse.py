import duckdb
import os
# from dotenv import load_dotenv
# load_dotenv()

DB_PATH = os.getenv("DUCKDB_PATH")

def query_job_listings(query='SELECT * FROM marts.mart_construction'):
    with duckdb.connect(DB_PATH, read_only=True) as conn:
        df = conn.query(query).df()
        df.columns = [c.upper() for c in df.columns]
    return df