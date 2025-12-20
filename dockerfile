FROM python:3.11-slim

ENV DUCKDB_PATH=/app/data_warehouse/job_ads.duckdb

WORKDIR /app/dashboard

COPY dashboard/ /app/dashboard/
COPY data_warehouse/ /app/data_warehouse/

RUN pip install --no-cache-dir streamlit duckdb pandas

EXPOSE 8501

CMD ["streamlit", "run", "dashboard.py", "--server.port=$PORT", "--server.address=0.0.0.0"]
