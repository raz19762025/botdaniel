import os
import json

import json
import requests
from environment_manager import load_env_chain

bought_tokens_path = "data/bought_tokens.json"
portfolio_path = "data/portfolio_status.json"

def load_bought_tokens():
    os.makedirs(os.path.dirname(bought_tokens_path), exist_ok=True)
    if not os.path.exists(bought_tokens_path):
        with open(bought_tokens_path, "w") as f:
            json.dump([], f)

    with open(bought_tokens_path, "r") as f:
        return json.load(f).get("tokens", [])

def load_portfolio_status():
    with open(portfolio_path, "r") as f:
        return json.load(f)

def save_portfolio_status(status):
    with open(portfolio_path, "w") as f:
        json.dump(status, f, indent=2)

def get_token_price(token_address):
    chain = load_env_chain()
    try:
        url = f"https://api.dexscreener.io/latest/dex/tokens/{chain}/{token_address}"
        res = requests.get(url, timeout=5)
        data = res.json()
        if data.get("pairs"):
            return float(data["pairs"][0].get("priceUsd", 0))
    except Exception:
        return 0
    return 0

def calculate_portfolio_value_usd(bought_tokens):
    total = 0
    for token in bought_tokens:
        price = get_token_price(token.get("token_address"))
        amount = token.get("amount_usd", 0)
        price_at_buy = token.get("buy_price_usd", price)
        if price_at_buy > 0:
            value_now = amount * (price / price_at_buy)
            total += value_now
        else:
            total += amount
    return total

def update_portfolio_status():
    tokens = load_bought_tokens()
    status = load_portfolio_status()
    current = calculate_portfolio_value_usd(tokens)
    status["current_value_usd"] = round(current, 2)
    status["is_target_reached"] = current >= status["initial_value_usd"] * (1 + status["target_profit_percent"])
    save_portfolio_status(status)
    return status
