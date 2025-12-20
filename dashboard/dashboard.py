import streamlit as st
import pandas as pd

from connect_data_warehouse import query_job_listings


def layout_graphs(df: pd.DataFrame, name: str) -> None:
    st.subheader(name)

    st.metric(
        label="Total vacancies",
        value=int(df["VACANCIES"].sum())
    )

    st.dataframe(df)


def main() -> None:
    st.set_page_config(page_title="Job Market Dashboard", layout="wide")

    st.title("Job Market Dashboard")

    # === Load data ===
    dashboard_df = query_job_listings()

    # ✅ KRITISK FIX: stoppa appen tidigt om data saknas
    if dashboard_df is None or dashboard_df.empty:
        st.error(
            "Data could not be loaded. "
            "The database or required tables are missing in this environment."
        )
        st.stop()

    # === Normal rendering ===
    name = "Construction Jobs"
    layout_graphs(dashboard_df, name)


if __name__ == "__main__":
    main()
