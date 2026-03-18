"""
Patrimo — Backend API
Lance avec : uvicorn api:app --reload --port 8000
"""

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
import yfinance as yf

app = FastAPI(title="Patrimo API", version="1.0.0")

# Autorise les appels depuis le navigateur (localhost)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["GET"],
    allow_headers=["*"],
)

# ─── Mapping crypto ticker → Yahoo Finance symbol ────────────────────
# yfinance utilise des paires comme BTC-EUR, ETH-EUR, etc.
CRYPTO_MAP = {
    "BTC":  "BTC-EUR",
    "ETH":  "ETH-EUR",
    "SOL":  "SOL-EUR",
    "XRP":  "XRP-EUR",
    "BNB":  "BNB-EUR",
    "DOGE": "DOGE-EUR",
    "ADA":  "ADA-EUR",
    "AVAX": "AVAX-EUR",
    "DOT":  "DOT-EUR",
    "MATIC":"MATIC-EUR",
    "LTC":  "LTC-EUR",
    "LINK": "LINK-EUR",
    "UNI":  "UNI-EUR",
    "ATOM": "ATOM-EUR",
    "ALGO": "ALGO-EUR",
}


@app.get("/")
def root():
    """Sert le fichier HTML principal"""
    return FileResponse("patrimoine.html")


@app.get("/api/price/{ticker}")
def get_price(ticker: str):
    """
    Retourne le prix actuel d'un titre ou d'une crypto en EUR.

    Exemples :
      /api/price/AAPL       → Action US
      /api/price/MC.PA      → Action française (Euronext Paris)
      /api/price/CW8.PA     → ETF Amundi MSCI World
      /api/price/IWDA       → iShares MSCI World (Euronext Amsterdam)
      /api/price/BTC        → Bitcoin en EUR (converti automatiquement)
      /api/price/ETH        → Ethereum en EUR
    """
    ticker = ticker.upper().strip()

    # Résoudre le bon symbole Yahoo Finance
    asset_type = "stock"
    yahoo_symbol = ticker

    if ticker in CRYPTO_MAP:
        yahoo_symbol = CRYPTO_MAP[ticker]
        asset_type = "crypto"

    try:
        yf_ticker = yf.Ticker(yahoo_symbol)
        info = yf_ticker.info

        # Récupérer le prix (plusieurs champs selon le type d'actif)
        price = (
            info.get("currentPrice")
            or info.get("regularMarketPrice")
            or info.get("previousClose")
        )

        if price is None:
            raise HTTPException(
                status_code=404,
                detail=f"Prix introuvable pour '{ticker}'. Vérifiez le symbole (ex: MC.PA, CW8.PA, BTC)."
            )

        currency = info.get("currency", "EUR")
        name = info.get("shortName") or info.get("longName") or ticker

        # Variation journalière
        prev_close = info.get("previousClose") or info.get("regularMarketPreviousClose")
        daily_change = None
        if prev_close and price and prev_close != 0:
            daily_change = round((price - prev_close) / prev_close * 100, 2)

        # Conversion en EUR si le titre est coté en autre devise
        price_eur = price
        fx_rate = None
        if currency not in ("EUR", "GBp"):  # GBp = pence, traité à part
            fx_symbol = f"{currency}EUR=X"
            try:
                fx = yf.Ticker(fx_symbol)
                fx_info = fx.info
                fx_rate = fx_info.get("regularMarketPrice") or fx_info.get("previousClose")
                if fx_rate:
                    price_eur = round(price * fx_rate, 4)
            except Exception:
                pass  # On garde le prix brut si la conversion échoue

        # Cas GBp (pence sterling) → convertir en GBP d'abord
        if currency == "GBp":
            price_gbp = price / 100
            fx = yf.Ticker("GBPEUR=X")
            fx_info = fx.info
            fx_rate = fx_info.get("regularMarketPrice")
            if fx_rate:
                price_eur = round(price_gbp * fx_rate, 4)
            currency = "GBP"

        return {
            "ticker": ticker,
            "yahoo_symbol": yahoo_symbol,
            "name": name,
            "price": price_eur,          # Toujours en EUR
            "price_raw": price,          # Prix brut dans la devise d'origine
            "currency": currency,
            "fx_rate": fx_rate,
            "daily_change": daily_change,
            "asset_type": asset_type,
            "source": "Yahoo Finance via yfinance",
        }

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Erreur lors de la récupération du prix : {str(e)}"
        )


@app.get("/api/health")
def health():
    return {"status": "ok", "message": "Patrimo API opérationnelle"}
