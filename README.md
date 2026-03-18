# 🏦 Patrimo — Suivi de patrimoine

Application de suivi de patrimoine avec **récupération automatique des cours** via `yfinance`.

## 📁 Structure

```
patrimo/
├── api.py            ← Serveur FastAPI (backend Python)
├── patrimoine.html   ← Interface web (frontend)
├── requirements.txt  ← Dépendances Python
├── start.sh          ← Script de lancement (Mac/Linux)
└── README.md
```

## 🚀 Lancement

### Prérequis
- Python 3.9+
- pip

### Installation & démarrage

```bash
# 1. Installer les dépendances
pip install -r requirements.txt

# 2. Lancer le serveur
uvicorn api:app --reload --port 8000

# Ou avec le script tout-en-un (Mac/Linux)
bash start.sh
```

### Accès
- **Application** : http://localhost:8000
- **API** : http://localhost:8000/api/price/{ticker}

---

## 📡 API — Exemples de tickers

| Type | Ticker | Exemple |
|------|--------|---------|
| Action française | `SYMBOL.PA` | `MC.PA` (LVMH) |
| Action US | `SYMBOL` | `AAPL`, `TSLA` |
| ETF Euronext Paris | `SYMBOL.PA` | `CW8.PA` (Amundi MSCI World) |
| ETF Euronext Amsterdam | `SYMBOL.AS` | `IWDA.AS` (iShares World) |
| ETF Frankfurt | `SYMBOL.DE` | `VWCE.DE` (Vanguard All-World) |
| Bitcoin | `BTC` | → converti automatiquement en EUR |
| Ethereum | `ETH` | → converti automatiquement en EUR |

### Exemple de réponse

```
GET /api/price/MC.PA
```

```json
{
  "ticker": "MC.PA",
  "name": "LVMH Moët Hennessy Louis Vuitton SE",
  "price": 612.5,
  "currency": "EUR",
  "daily_change": -0.84,
  "source": "Yahoo Finance via yfinance"
}
```

---

## ⚠️ Limites

- Les prix sont **différés d'environ 15 minutes** (suffisant pour un suivi perso)
- `yfinance` n'est pas une API officielle — peut parfois être instable
- Les bourses asiatiques ont une couverture limitée
