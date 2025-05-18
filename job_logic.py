
import json
import logging
from settings import TELEGRAM_CHAT_ID, PROFIT_THRESHOLD
from scanner import scan_market
from trade_executor import execute_buy, execute_sell
from portfolio_tracker import update_portfolio_status
from tradingview_signal import get_tradingview_signal

BOUGHT_TOKENS_PATH = "data/bought_tokens.json"

def load_bought_tokens():
    try:
        with open(BOUGHT_TOKENS_PATH, "r") as f:
            return json.load(f).get("tokens", [])
    except:
        return []

def save_bought_tokens(tokens):
    with open(BOUGHT_TOKENS_PATH, "w") as f:
        json.dump({"tokens": tokens}, f, indent=2)

async def job(context):
    status = update_portfolio_status()
    from report_generator import append_history
    append_history(status["current_value_usd"])
    if status["is_target_reached"]:
        await context.bot.send_message(
            chat_id=TELEGRAM_CHAT_ID,
            text="✅ Daily profit target reached. No more buys today."
        )
        return

    logging.info("🔄 Job triggered")
    pairs = scan_market_all()
    bought_tokens = load_bought_tokens()

    winners = [c for c in pairs if c['change'] >= PROFIT_THRESHOLD]
    new_trades = 0

    for coin in winners:
        token_address = coin['token_address']
        already_bought = any(t['token_address'] == token_address for t in bought_tokens)
        if already_bought:
            continue

        symbol = coin['symbol'].upper()
        signal = get_tradingview_signal(symbol)
        if signal != "buy":
            continue  # לא קונים אם אין המלצה מ-TradingView

        try:
            tx = execute_buy(token_address, "buy", amount_eth=0.01)
            if tx:
                await context.bot.send_message(
                    chat_id=TELEGRAM_CHAT_ID,
                    text=f"✅ BUY: {coin['symbol']} (${coin['price']:.4f}) | TV Signal: {signal} | TX: {tx}"
                )
                bought_tokens.append({
                    "token_address": token_address,
                    "amount_usd": coin['price'] * 0.01 * 1,
                    "buy_price_usd": coin['price'],
                    "symbol": coin['symbol']
                })
                new_trades += 1
        except Exception as e:
            await context.bot.send_message(
                chat_id=TELEGRAM_CHAT_ID,
                text=f"❌ Error buying {coin['symbol']}: {str(e)}"
            )

    save_bought_tokens(bought_tokens)

    if new_trades == 0:
        await context.bot.send_message(
            chat_id=TELEGRAM_CHAT_ID,
            text="📭 No new buys. Either already bought, or no TV signal."
        )
