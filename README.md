Automation DevOps Pipeline – Examination

Detta projekt demonstrerar en fullständig CI/CD-pipeline byggd med GitHub Actions, Docker, DockerHub, Azure Web App for Containers, samt pytest, dlt och dbt.
Projektet uppfyller samtliga krav i kursens examinationsuppgift och implementerar ett komplett DevOps-flöde från kod → test → build → datahantering → visualisering → deployment.

1. Översikt

Projektet består av fem separata pipelines som körs i en kedja:

Python CI
Kör lint + pytest + artefaktloggning (villkorlig).
Startar automatiskt vid push till utvecklingsbranchen.

DLT Pipeline
Körs automatiskt när Python CI lyckas.
Extraherar / transformeras data med dlt.

dbt Pipeline
Körs när DLT Pipeline lyckas.
Bygger datamodeller i dbt.

Build docker image
Körs när dbt Pipeline lyckas.
Bygger och pushar Docker-imaget (sha-tag + latest) till DockerHub.

Deploy to Azure Web App (Docker Native)
Körs när Build docker image lyckas.
Konfigurerar Azure App Service att köra senaste Docker-imagen.

Varje pipeline använder workflow_run för att skapa beroenden mellan workflows.

2. Mappstruktur
.
├── app/
│   ├── logic.py              # Enkel logikmodul för unit testing
│   └── __init__.py
│
├── dashboard/
│   └── dashboard.py          # Streamlit dashboard
│
├── data_warehouse/
│   └── job_ads.duckdb        # DuckDB-fil
│
├── tests/
│   ├── test_logic.py
│   ├── test_string_utils.py
│   └── test_repo_smoke.py
│
├── Dockerfile
├── requirements.txt
└── .github/
    └── workflows/
        ├── python-ci.yml
        ├── dlt-pipeline.yml
        ├── dbt-pipeline.yml
        ├── build-docker-image.yml
        └── deploy.yml
