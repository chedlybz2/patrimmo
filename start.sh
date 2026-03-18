#!/bin/bash
# ─── Patrimo — Script de lancement ───────────────────────────────────

echo ""
echo "  🏦  Patrimo — Suivi de patrimoine"
echo "  ──────────────────────────────────"
echo ""

# 1. Vérifier que Python est disponible
if ! command -v python3 &> /dev/null; then
    echo "  ❌ Python3 introuvable. Installez Python 3.9+ depuis https://python.org"
    exit 1
fi

# 2. Installer les dépendances si nécessaire
echo "  📦 Vérification des dépendances..."
pip install -r requirements.txt -q

# 3. Lancer le serveur
echo ""
echo "  ✅ Serveur démarré !"
echo "  👉 Ouvrez votre navigateur sur : http://localhost:8000"
echo "  📡 API disponible sur          : http://localhost:8000/api/price/MC.PA"
echo ""
echo "  Ctrl+C pour arrêter"
echo ""

uvicorn api:app --host 0.0.0.0 --port 8000 --reload
