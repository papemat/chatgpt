# TokIntel API – Deploy & Usage

## 🚀 Avvio rapido con Docker

### 1. Build dell'immagine
```bash
docker build -t tokintel-api .
```

### 2. Avvio con Docker Compose
```bash
docker compose up
```

L'API sarà disponibile su [http://localhost:8000](http://localhost:8000)

### 3. Esportazione e download
- Tutti i file esportati saranno disponibili nella cartella `src/api/downloads` (montata come volume)

### 4. Test automatici
```bash
docker exec -it tokintel-api pytest src/api/tests/ -v
```

### 5. Documentazione API
- Swagger/OpenAPI: [http://localhost:8000/docs](http://localhost:8000/docs)

---

## 📦 Struttura principale

- `Dockerfile` – build e run API
- `docker-compose.yml` – gestione servizi e volumi
- `src/api/` – codice FastAPI, endpoint, test
- `src/api/downloads/` – output file esportati

---

## 🔒 Note
- Per ambienti di produzione, personalizza variabili d'ambiente e sicurezza.
- Puoi estendere il compose per aggiungere database, cache, ecc. 