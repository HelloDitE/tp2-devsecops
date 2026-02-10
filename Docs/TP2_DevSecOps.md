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
{"status":"ok"}```

(curl.exe -i http://localhost:5001/health sur windows)


## Partie B : Logs Structurés (JSON)

Pour permettre une analyse automatisée (Gate Runtime), nous avons remplacé les logs textuels par défaut de Flask par des logs structurés au format JSON.

### 1. Implémentation (`app.py`)
Nous avons utilisé les middlewares Flask `before_request` et `after_request` pour :
* **Générer un Request-ID :** Un UUID unique est attribué à chaque requête (ou récupéré via le header `X-Request-Id`) pour la traçabilité.
* **Mesurer la latence :** Calcul du temps d'exécution en millisecondes (`latency_ms`).
* **Formatter en JSON :** Chaque ligne de log contient désormais : `ts`, `level`, `service`, `request_id`, `method`, `path`, `status`, `latency_ms`.

### 2. Preuve de fonctionnement
Les logs du conteneur sont maintenant lisibles par une machine.

**Exemple de log capturé :**
```json
{
  "ts": "2026-02-10T10:00:00Z",
  "level": "INFO",
  "service": "catalog",
  "request_id": "a1b2c3d4-...",
  "method": "GET",
  "path": "/health",
  "status": 200,
  "latency_ms": 1,
  "query": ""
}


## Partie C : Générateur de Trafic

Pour alimenter les logs et tester nos détecteurs en conditions réelles, nous avons mis en place un générateur de trafic automatisé.

### 1. Script (`monitoring/traffic.sh`)
Ce script Bash permet de simuler deux types d'activité sur l'application :
* [cite_start]**Trafic Normal :** Une boucle de requêtes sur `/health` et `/search` pour simuler une utilisation légitime [cite: 318-321].
* **Trafic Suspect (Attaques) :** Activé via la variable d'environnement `SUSPECT_MODE=1`. Il envoie des requêtes malveillantes contenant des tentatives de **Path Traversal** (`../../etc/passwd`) et d'**Injection de Commande** (`cmd=id`) [cite: 324-328].

### 2. Validation
Nous avons validé que l'exécution du script génère bien des entrées correspondantes dans les logs JSON du conteneur.

**Commandes utilisées :**
```bash
# Trafic normal
bash monitoring/traffic.sh

# Trafic d'attaque
SUSPECT_MODE=1 bash monitoring/traffic.sh