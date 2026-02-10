import time
import uuid
import json
from flask import Flask, request, g, jsonify

app = Flask(__name__)
SERVICE_NAME = "catalog"

# 1. Avant la requête : On démarre le chronomètre et on gère l'ID
@app.before_request
def _before():
    # Temps de départ pour calculer la latence
    g.start_time = time.time()
    
    # Récupération ou création du Request-ID
    rid = request.headers.get("X-Request-Id")
    if not rid:
        rid = str(uuid.uuid4())
    g.request_id = rid

# 2. Après la requête : On calcule et on logge en JSON
@app.after_request
def _after(response):
    # Calcul de la latence en millisecondes
    latency_ms = int((time.time() - g.start_time) * 1000)
    
    # Construction du log structuré
    record = {
        "ts": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
        "level": "INFO",
        "service": SERVICE_NAME,
        "request_id": g.request_id,
        "method": request.method,
        "path": request.path,
        "status": response.status_code,
        "latency_ms": latency_ms,
        # On tronque la query string pour éviter les logs trop longs
        "query": (request.query_string.decode("utf-8")[:200] if request.query_string else ""),
    }
    
    # Affichage du JSON dans la console (flush=True pour que Docker le voie tout de suite)
    print(json.dumps(record), flush=True)
    
    # On renvoie l'ID au client dans les headers
    response.headers["X-Request-Id"] = g.request_id
    return response

@app.route('/health')
def health():
    return jsonify({"status": "ok"}), 200

@app.route('/')
def index():
    return "Catalog Service Ready"

# Ajout de la route search pour tester les query params plus tard
@app.route('/search')
def search():
    return jsonify({"results": []}), 200

# Ajout d'une route debug pour simuler les attaques plus tard
@app.route('/debug/run')
def debug_run():
    return jsonify({"output": "fake output"}), 200

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)