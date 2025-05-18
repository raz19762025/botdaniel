
import requests
import time
import logging

GECKO_API = "https://api.geckoterminal.com/api/v2/networks/bsc/pools"

def scan_market_gecko():
    try:
        res = requests.get(GECKO_API, timeout=10)
        data = res.json()
    except Exception as e:
        logging.error(f"Gecko scan error: {e}")
        return []

    results = []
    now = int(time.time())
    for pool in data.get("data", []):
        try:
            attrs = pool["attributes"]
            token = attrs["base_token"]
            token_address = token.get("address", "")
            symbol = token.get("symbol", "")
            price = float(attrs.get("price_usd", 0))
            volume = float(attrs.get("volume_usd", 0))
            liquidity = float(attrs.get("reserve_in_usd", 0))
            change = float(attrs.get("price_change_percentage", {}).get("h1", 0)) / 100

            results.append({
                "symbol": symbol,
                "price": price,
                "token_address": token_address,
                "liquidity": liquidity,
                "volume": volume,
                "change": change
            })
        except Exception:
            continue

    logging.info(f"Scanned {len(results)} pools from GeckoTerminal")
    return results
