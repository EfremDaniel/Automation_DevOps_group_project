import os
from pathlib import Path

import duckdb


DB_PATH = os.getenv("DUCKDB_PATH")


def query_job_listings(query="SELECT * FROM marts.mart_construction"):
    if DB_PATH is None:
        return None

    Path(DB_PATH).parent.mkdir(parents=True, exist_ok=True)

    try:
        with duckdb.connect(DB_PATH, read_only=False) as conn:
            df = conn.query(query).df()
            df.columns = [c.upper() for c in df.columns]
            return df
    except Exception:
        # Tom databas / saknad tabell – tillåtet i Azure
        return None
