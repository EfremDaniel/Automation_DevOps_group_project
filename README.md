# Individuell Rapport – CI/CD Pipeline

## 1. Beskrivning av min pipeline

Min pipeline är uppdelad i flera separata workflows i GitHub Actions. Syftet är att automatisera testning, datasteg, container-bygge och distribution till Azure. Varje workflow har ett tydligt ansvar och workflows kopplas ihop med `workflow_run` för att skapa ett sekventiellt flöde där nästa steg endast körs när föregående lyckats.

### **Python CI (testning och kodvalidering)**
Detta workflow körs vid push eller manuellt. Det innehåller:
- Installation av Python och beroenden  
- Linting med flake8  
- Testkörning med pytest  
- Villkorlig uppladdning av loggar vid fel  
- Sättning av en output-variabel som anger om testerna passerade

Detta säkerställer kvalitet tidigt i kedjan.

### **DLT Pipeline**
Workflowet kör dataladdning eller transformation. Det används för att validera datasteg innan modellering och distribution sker. Vid fel laddas loggar upp.

### **DBT Pipeline**
Körs endast om DLT Pipeline lyckas. Steg:
- Installation av dbt-core och duckdb  
- Injektering av `profiles.yml` via GitHub Secrets  
- dbt debug, deps och build  
- Loggar laddas upp vid fel

Detta validerar datamodellerna och säkerställer struktur innan applikationen byggs.

### **Docker Build Workflow**
Körs när DBT Pipeline är klar. Steg:
- Docker login (Docker Hub)  
- Bygge av image med både `latest` och commit-SHA-tag  
- Push av båda taggarna

Syftet är att skapa en reproducerbar container per commit och en stabil latest-version.

### **Deploy Workflow (Azure Web App – Docker)**
Det sista workflowet deployar containerimagen till Azure. Det innefattar:
- Inloggning i Azure med service principal  
- Uppdatering av App Service att använda rätt Docker-image  
- Eventuell uppdatering av PORT/app settings  
- Omdirigering av trafik genom restart

Detta workflow representerar CD-steget i pipelinen.

---

## 1.b Motivering av designval

### **Separata workflows**
Jag delade upp pipelinen i flera workflows för att följa principer om moduläritet, spårbarhet och stabilitet. Ett fel i t.ex. teststeget ska inte leda till onödig körning av bygg- eller deploysteg. Varje workflow kan felsökas individuellt.

### **Användning av `workflow_run`**
Jag använde `workflow_run` för att bygga en kedja:
