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

3. Tester (Unit Tests)

Enhetstester körs i Python CI-workflowet.
Tester testas med pytest.

Exempel från projektets tester:
from app.logic import normalize_text, add_numbers

def test_normalize_text_basic():
    assert normalize_text(" HeLLo ") == "hello"

def test_add_numbers():
    assert add_numbers(2, 3) == 5

Villkorlig loggning

Workflowet använder:

workflow_dispatch:
  log_errors: true/false


Om log_errors = true och tester misslyckas → genereras loggar (pytest_output.txt) som artefakt.

4. Docker & DockerHub

När alla data- och modellsteg lyckas byggs en Docker-image:

Taggas som:

<user>/myapp:latest

<user>/myapp:<commit_sha>

Pushas till DockerHub med docker/login-action@v3.

Dockerfile används för att köra en Streamlit-applikation:

FROM python:3.11-slim
WORKDIR /app/dashboard
COPY dashboard/ /app/dashboard/
COPY data_warehouse/ /app/data_warehouse/
RUN pip install streamlit duckdb pandas
CMD ["streamlit", "run", "dashboard.py", "--server.port=8501", "--server.address=0.0.0.0"]


(Porten 8501 sätts i Azure via WEBSITES_PORT=8501.)

5. Azure Deployment (Docker Native)

Azure-deploy använder:

azure/login@v1 (med Service Principal)

az webapp config container set

az webapp restart

Secrets:

AZURE_CREDENTIALS
AZURE_WEBAPP_NAME
AZURE_RESOURCE_GROUP
DOCKERHUB_USERNAME
DOCKERHUB_TOKEN


Appen konfigureras med den nya Docker-imagen automatiskt.

6. GitHub Secrets (sammanfattning)
Secret	Beskrivning
DOCKERHUB_USERNAME	DockerHub-användarnamn
DOCKERHUB_TOKEN	DockerHub personal access token
AZURE_CREDENTIALS	JSON från az ad sp create-for-rbac --sdk-auth
AZURE_WEBAPP_NAME	Namnet på App Service
AZURE_RESOURCE_GROUP	Resource Group i Azure
7. Triggers & beroenden

Varje workflow körs automatiskt efter det föregående:

Python CI
→ DLT Pipeline
→ dbt Pipeline
→ Build Image
→ Deploy

Implementation via:

on:
  workflow_run:
    workflows: ["Previous workflow"]
    types: [completed]


Varje jobb använder:

if: ${{ github.event.workflow_run.conclusion == 'success' }}


för att endast fortsätta vid success.

8. DevOps-principer som uppfylls

CI: Automated testing, linting

CD: Automated build, push, deploy

Observability: Villkorlig loggning vid testfel

Infrastructure as Code: GitHub Actions YAML

Isolation & reproducibility: Docker images, pinned Python versions

Secrets management: GitHub Secrets

Dependency chaining: workflow_run + if-satser

Automation: full pipeline från push → deployment

9. Hur man kör projektet lokalt

Installera dependencies:

pip install -r requirements.txt


Starta Streamlit-dashboard:

streamlit run dashboard/dashboard.py


Kör tester:

pytest -q

10. Sammanfattning

Detta projekt implementerar:

en fungerande och komplett CI/CD-pipeline

datainhämtning (DLT)

datamodellering (dbt)

visualisering (Streamlit)

containerisering (Docker)

hosting & deployment (Azure App Service)

Alla steg är automatiserade och kedjade med beroenden enligt kursens examinationskrav.
