#!/bin/bash
set -euo pipefail
BASE_URL="${BASE_URL:-http://localhost:5001}"

echo "[traffic] Sending normal traffic to $BASE_URL..."

# 1. Trafic de fond (Healthchecks) - Boucle 30 fois
for i in $(seq 1 30); do
    curl -fsS "$BASE_URL/health" >/dev/null
done

# 2. Trafic applicatif (Recherches)
# Le "|| true" permet de ne pas planter le script si la requête échoue
curl -s "$BASE_URL/search?q=abc" >/dev/null || true
curl -s "$BASE_URL/search?q=test" >/dev/null || true

# 3. Mode "Suspect" (Activé seulement si la variable SUSPECT_MODE=1)
# Cela simule des attaques pour tester notre future Gate de sécurité
if [ "${SUSPECT_MODE:-0}" = "1" ]; then
    echo "[traffic] !!! GENERATING SUSPECT TRAFFIC !!!"
    # Simulation Path Traversal (accès fichier sensible)
    curl -s "$BASE_URL/report?file=../../etc/passwd" >/dev/null || true
    # Simulation Injection de Commande
    curl -s "$BASE_URL/debug/run?cmd=id" >/dev/null || true
fi

echo "[traffic] Done."