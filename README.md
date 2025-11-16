# Individuell Rapport – CI/CD Pipeline

## 1. Beskrivning av min pipeline

Min pipeline består av flera separata GitHub Actions-workflows som tillsammans bildar ett helt CI/CD-flöde. Varje workflow har ett tydligt syfte och kedjas ihop med `workflow_run`, vilket skapar en sekventiell pipeline där nästa steg endast körs om föregående lyckas.

### 1.a Jobb och steps i min pipeline

**Python CI**  
- Installerar Python och beroenden  
- Kör flake8  
- Kör pytest  
- Loggar laddas upp vid fel (enligt `log_errors`-parametern)  
- Output sätts för att meddela om testerna passerade  

**DLT Pipeline**  
- Kör dataladdning/transformering  
- Vid fel laddas loggar upp  

**DBT Pipeline**  
- Installerar dbt och skriver `profiles.yml` från Secret  
- Kör dbt debug, deps och build  
- Loggar laddas upp vid fel  

**Docker Build**  
- Loggar in på Docker Hub  
- Bygger image med både latest-tag och SHA-tag  
- Pushar båda bilderna  

**Deploy till Azure**  
- Loggar in i Azure via Service Principal  
- Pekar App Service mot senaste Docker-image  
- Uppdaterar settings vid behov (t.ex. PORT 8501)  
- Restartar appen  

Pipeline följer strukturen:

