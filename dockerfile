FROM python:3.11-slim

ENV DUCKDB_PATH=/app/data_warehouse/job_ads.duckdb
ENV STREAMLIT_SERVER_ADDRESS=0.0.0.0

WORKDIR /app/dashboard

COPY dashboard/ /app/dashboard/
COPY data_warehouse/ /app/data_warehouse/

RUN pip install --no-cache-dir streamlit duckdb pandas

EXPOSE 8501

CMD ["sh", "-c", "export STREAMLIT_SERVER_PORT=$PORT && streamlit run dashboard.py"]
