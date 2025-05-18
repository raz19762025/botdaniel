
import requests

def get_tradingview_signal(symbol: str, interval: str = "1h") -> str:
    try:
        url = f"https://scanner.tradingview.com/crypto/scan"
        headers = {"content-type": "application/json"}
        payload = {
            "symbols": {
                "tickers": [f"BINANCE:{symbol}USDT"],
                "query": {"types": []}
            },
            "columns": ["Recommend.All"]
        }
        res = requests.post(url, json=payload, headers=headers, timeout=5)
        data = res.json()
        rec = data["data"][0]["d"][0]
        if rec >= 0.5:
            return "buy"
        elif rec <= -0.5:
            return "sell"
        else:
            return "neutral"
    except Exception:
        return "unknown"
