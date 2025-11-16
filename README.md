# Individuell Rapport – CI/CD Pipeline

## 1. Beskrivning av min pipeline

Min pipeline består av flera separata GitHub Actions-workflows som tillsammans bygger ett komplett CI/CD-flöde. Syftet är att automatisera testning, datasteg, byggprocess och distribution av en containeriserad applikation till Azure. Jag valde att bryta upp pipelinen i flera delar eftersom det gav bättre kontroll, tydligare felsökning och mindre risk att hela processen faller vid ett enda fel.

---

## 1.a Jobb och steps i min pipeline

### **Python CI**
Detta workflow körs vid push och manuellt. Det säkerställer kodkvalitet innan något annat steg exekveras.

**Steps:**
- **Setup Python** – skapar en definierad och stabil miljö.
- **Install dependencies** – installerar alla krav, inklusive linting och testbibliotek.
- **Linting (flake8)** – säkerställer att koden följer standarder och inte innehåller enkla fel.
- **Pytest** – kör enhetstest och skriver loggar vid fel.
- **Villkorlig loggupload** – uppgiften krävde att loggar endast laddas upp när fel inträffar.

Detta steg fungerar som "gate" för hela pipelinen.

---

### **DLT Pipeline**
Körs när teststeget är grönt. Den ansvarar för dataladdning eller transformering innan modellering.

**Steps (sammanfattat):**
- Setup miljö
- Installera nödvändiga bibliotek
- Kör DLT-script
- Loggning och uppladdning vid fel

Detta steg säkerställer att datagrundlagret fungerar innan modellen byggs.

---

### **DBT Pipeline**
Startar endast vid lyckad DLT-körning. DBT validerar och bygger datamodeller.

**Steps:**
- Installera dbt-core och dbt-duckdb
- Skriva `profiles.yml` från secret (för att pipelinen ska vara säker)
- `dbt debug`, `dbt deps`, `dbt build`
- Loggupp­laddning vid fel

Detta steg bekräftar att datamodeller är korrekta innan image-bygget.

---

### **Docker Build Workflow**
Startas efter DBT Pipeline.

**Steps:**
- Docker login till Docker Hub
- Bygger image från Dockerfile
- Taggar både `latest` och commit-SHA
- Pushar båda bilderna

Detta steg gör varje commit reproducerbar och förbereder den för deployment.

---

### **Deploy Workflow**
Detta workflow hanterar distributionen till Azure.

**Steps:**
- Azure Login via Service Principal
- Konfigurera Web App med rätt Docker-image
- Sätta App Settings vid behov (t.ex. PORT)
- Restart av tjänsten

Detta steg säkerställer att den senaste godkända versionen körs i molnet.

---

## 1.b Motivering av designval

- **Separerade workflows** ger tydligare logik, bättre felsökning och gör att fel inte sprids vidare.  
- **workflow_run** används för att skapa ett kontrollerat flöde där varje del måste lyckas innan nästa körs.  
- **Villkorlig loggning** följer projektkraven och bevarar resurser.  
- **Docker** valdes för att säkerställa konsekvent miljö — allt körs identiskt lokalt, i Actions och i Azure.  
- **Azure App Service (Linux + Container)** valdes för enkel koppling till CI/CD och för att det stödjer containerbaserad deployment.

---

## 1.c Fel jag stötte på och hur jag felsökte

Under projektet stötte jag på många problem som tog mycket tid. Detta gjorde att jag inte hann slutföra exakt alla delar så som jag först planerade, men jag dokumenterar här de viktigaste felen och min felsökning.

### **1. YAML‐problem i GitHub Actions**
Flera workflows bröt på grund av:
- indenteringsfel  
- felaktiga outputs  
- bortglömda parametrar  

**Felsökning:**  
Jag läste Actions-loggar, använde YAML-validatorer och jämförde med documentation.

---

### **2. Docker Hub inloggningsfel**
`unauthorized` och `incorrect username or password`.

**Orsak:** felaktigt token/värde i Secret.  
**Lösning:** skapa nytt access token i Docker Hub och uppdatera GitHub Secrets.

---

### **3. Azure kunde inte hämta bilden**
Fel som:
manifest unknown
pull access denied
repository not found


**Orsak:**  
Fel i App Service-konfiguration:
- fel “Registry server URL”  
- saknade credentials  
- fel image path (t.ex. saknat namespace)  

**Lösning:**  
- använda `index.docker.io`  
- ange `efrem27/myapp:latest`  
- lägga in Docker Hub access token i App Service

---

### **4. App Service var Windows och stödde inte Docker korrekt**
Eftersom första App Service var Windows-baserad fanns inte:
- Container settings  
- Log Stream  
- Container start command  
- Rätt inställningar för PORT  

**Lösning:**  
Skapa ny **Linux Web App for Containers**, vilket löste problemet.

---

### **5. workflow_run triggas inte**
GitHub Actions triggar inte workflow_run om workflowet själv startats av workflow_run.

**Lösning:**  
Köra build manuellt eller via push samt anpassa triggers.

---

## 2. Självreflektion

### 2.a Min egen insats och utmaningar

Jag mötte många tekniska problem, speciellt kring Azure-konfiguration, Docker Hub tokens och GitHub Actions-triggers. Detta gjorde att jag inte hann genomföra allt exakt så som jag först tänkt, men arbetet gav mig djup förståelse för hur verkliga pipelines beter sig.

Jag lärde mig:
- hur små syntaxfel i YAML kan bryta hela pipelinen  
- hur viktigt det är att ha rätt credentials och secrets  
- hur man felsöker logs, Actions och Azure-tjänster  
- vikten av att dela upp pipelines i mindre delar  
- varför DevOps kräver tålamod och struktur  

Trots problemen anser jag att jag fick en bra helhetsbild och blev betydligt tryggare i CI/CD-arbete.

---

### 2.b Mina lärdomar om DevOps

Under kursen och projektet fick jag bättre förståelse för:

- **DevOps som kultur:** samarbete, delat ansvar och snabb återkoppling.  
- **Principer:** automation, kontinuitet, mätbarhet, kvalitet och skalbarhet.  
- **Viktiga termer:** CI, CD, workflows, artifacts, runners, containers, logs.  
- **Pipelines:** hur testning, byggprocess och deployment binds ihop i ett flöde.  
- **Containers:** varför Docker och containerisering är centralt i modern DevOps.  
- **Azure:** hur molnplattformar integrerar med CI/CD.

Det gav en praktisk förståelse för hur DevOps tillämpas i riktiga projekt.

---

## Sammanfattning

Jag byggde en komplett pipeline som automatiserar testning, datasteg, containerbygge och distribution. Även om jag stötte på flera problem och inte hann allt i tid, fick jag en djup förståelse för DevOps-arbete, pipelines, felsökning och hur man bygger en hållbar CI/CD-lösning.


