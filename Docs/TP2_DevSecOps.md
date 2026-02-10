# TP2 DevSecOps : Monitoring et Gate Runtime

## Partie A : Initialisation de l'environnement Staging

Nous avons mis en place un environnement minimaliste pour servir de base au monitoring.

### 1. Architecture
- **Service :** Catalog (Flask)
- **Port exposé :** 5001
- **Orchestration :** Docker Compose (`compose.staging.yml`)

### 2. Vérification du déploiement
Le service expose une route `/health` fonctionnelle.

**Preuve de fonctionnement :**
```bash
$ curl -i http://localhost:5001/health
HTTP/1.1 200 OK
...
{"status":"ok"}