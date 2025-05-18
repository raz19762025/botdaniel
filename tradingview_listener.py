
from fastapi import FastAPI, Request
from trade_executor import execute_trade

tv_app = FastAPI()

@tv_app.post("/tv-webhook")
async def tradingview_hook(request: Request):
    data = await request.json()
    token = data.get("token")
    action = data.get("action", "buy")
    amount = float(data.get("amount_eth", 0.01))

    if not token:
        return {"error": "No token provided"}

    tx = execute_trade(token, action, amount_eth=amount)
    return {"status": "success", "tx": tx}
