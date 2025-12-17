import os
from pathlib import Path
import duckdb



DB_PATH = os.getenv("DUCKDB_PATH")



def query_job_listings(query='SELECT * FROM marts.mart_construction'):
    Path(DB_PATH).parent.mkdir(parents=True, exist_ok=True)

    with duckdb.connect(DB_PATH, read_only=False) as conn:
        try:
            df = conn.query(query).df()
            df.columns = [c.upper() for c in df.columns]
            return df
        except Exception as e:
            # Tom databas / saknad tabell – tillåtet i Azure
            return None