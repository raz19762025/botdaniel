
import requests
import logging
from environment_manager import load_env_chain

COINGECKO_URL = "https://api.coingecko.com/api/v3/coins/markets"
PARAMS = {
    "vs_currency": "usd",
    "order": "volume_desc",
    "per_page": 50,
    "page": 1,
    "sparkline": False
}

def scan_market():
    results = []
    try:
        res = requests.get(COINGECKO_URL, params=PARAMS, timeout=10)
        tokens = res.json()
        logging.info(f"🧪 CoinGecko returned {len(tokens)} tokens")
    except Exception as e:
        logging.error(f"❌ Failed to fetch from CoinGecko: {e}")
        return []

    for token in tokens:
        try:
            symbol = token.get("symbol", "???").upper()
            name = token.get("name", "unknown")
            price = float(token.get("current_price", 0))
            volume = float(token.get("total_volume", 0))
            change = float(token.get("price_change_percentage_24h", 0)) / 100
            token_address = token.get("id", "coingecko")

            results.append({
                "symbol": symbol,
                "name": name,
                "price": price,
                "token_address": token_address,
                "volume": volume,
                "liquidity": 0,
                "change": change
            })
        except Exception:
            continue

    logging.info(f"✅ Parsed {len(results)} CoinGecko tokens")
    return results
