import json
import os

POSITIONS_FILE = "data/positions.json"

def load_positions():
    if os.path.exists(POSITIONS_FILE):
        try:
            return json.load(open(POSITIONS_FILE))
        except Exception:
            return {}
    return {}

def save_positions(positions):
    directory = os.path.dirname(POSITIONS_FILE)
    if directory and not os.path.exists(directory):
        os.makedirs(directory)
    with open(POSITIONS_FILE, "w") as f:
        json.dump(positions, f, indent=2)

def add_position(token_address, amount_eth, purchase_price):
    positions = load_positions()
    positions[token_address] = {
        "amount_eth": amount_eth,
        "purchase_price": purchase_price
    }
    save_positions(positions)

def remove_position(token_address):
    positions = load_positions()
    if token_address in positions:
        del positions[token_address]
        save_positions(positions)

class PortfolioTracker:
    def get_value(self):
        # TODO: implement actual portfolio valuation
        return 1.0

class RiskManager:
    def __init__(self, max_portfolio_risk=0.2):
        self.portfolio = PortfolioTracker()
        self.max_risk = max_portfolio_risk

    def calculate_position_size(self, token_risk_score):
        portfolio_value = self.portfolio.get_value()
        allowed_risk = portfolio_value * self.max_risk
        return allowed_risk * (1 - token_risk_score)
