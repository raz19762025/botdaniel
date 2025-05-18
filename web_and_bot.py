from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
import logging
import logging
from job_logic import update_portfolio_status
from src.execution import TradeManager
from report_generator import append_history
from src.ai_pipeline import predict_next
from trade_executor import execute_buy, execute_sell
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes
from telegram.ext import CommandHandler
from settings import TELEGRAM_BOT_TOKEN, TELEGRAM_CHAT_ID, PROFIT_THRESHOLD
from scanner import scan_market
from scanner_async import scan_market_all_async
from scanner_async import scan_market_all_async
from report_generator import compute_report
from trade_executor import execute_buy, execute_sell

async def start_command(update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(chat_id=TELEGRAM_CHAT_ID, text="✅ Bot is up and running")

async def status_command(update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(
        chat_id=TELEGRAM_CHAT_ID,
        text=f"📊 Profit threshold: {PROFIT_THRESHOLD * 100}%"
    )

async def chains_command(update, context: ContextTypes.DEFAULT_TYPE):
    # chain info not available in scan_market output
    await context.bot.send_message(
        chat_id=TELEGRAM_CHAT_ID,
        text="🌐 Chain info not available."
    )

async def job(context: ContextTypes.DEFAULT_TYPE):
    logging.info("🔄 Job triggered")
    pairs = await scan_market_all_async()
    await context.bot.send_message(
        chat_id=TELEGRAM_CHAT_ID,
        text=f"🔄 Scanned {len(pairs)} pairs; sample: {[c['symbol'] for c in pairs[:5]]}"
    )
    winners = [c for c in pairs if c['change'] >= PROFIT_THRESHOLD]
    if winners:
        await context.bot.send_message(
            chat_id=TELEGRAM_CHAT_ID,
            text=f"🚀 Coins above threshold: {[c['symbol'] for c in winners]}"
        )
        for coin in winners:
            try:
                tx = execute_buy(coin['token_address'], "buy", amount_eth=0.01)
                if tx:
                    await context.bot.send_message(
                        chat_id=TELEGRAM_CHAT_ID,
                        text=f"✅ Trade executed for {coin['symbol']}: {tx.hex()}"
                    )
            except Exception as e:
                msg = str(e)
                if "no data" in msg:
                    logging.debug(f"Skipped no-data error for {coin['symbol']}")
                    continue
                await context.bot.send_message(
                    chat_id=TELEGRAM_CHAT_ID,
                    text=f"🔴 Trade error for {coin['symbol']}: {msg}"
                )


async def report_command(update, context: ContextTypes.DEFAULT_TYPE):
    arg = (context.args[0].lower() if context.args else "daily")
    mapping = {"daily":1, "weekly":7, "monthly":30}
    days = mapping.get(arg, 1)
    rpt = compute_report(days)
    if not rpt:
        text = f"אין מספיק נתונים לדוח {arg}"
    else:
        text = (
            f"דוח {arg} ({rpt['from']}→{rpt['to']}):\n"
            f"מ- {rpt['start']}$ → עד {rpt['end']}$\n"
            f"שינוי: {rpt['change_pct']}%"
        )
    await context.bot.send_message(chat_id=TELEGRAM_CHAT_ID, text=text)

from src.ai_pipeline import predict_next
from src.execution import TradeManager

async def ai_daily(update, context: ContextTypes.DEFAULT_TYPE):
    status = update_portfolio_status()
    capital = status["current_value_usd"]
    tm = TradeManager(capital)
    append_history(capital)
    market = await scan_market_all_async()
    msg = []
    for token in market:
        pred = predict_next(token["symbol"])
        size = tm.calc_position_size(pred)
        if size < 1e-6 or tm.target_reached():
            continue
        msg.append(f"{token['symbol']}: צפוי {pred*100:.1f}% → גודל {size:.2f}$")
    await context.bot.send_message(chat_id=update.effective_chat.id, text="🤖 הצעות לעיסקה:\n" + "\n".join(msg))
def start_bot():
    logging.basicConfig(level=logging.INFO)
    app = ApplicationBuilder().token(TELEGRAM_BOT_TOKEN).build()
    app.add_handler(CommandHandler("ai_daily", ai_daily))
    app.add_handler(CommandHandler("start", start_command))
    app.add_handler(CommandHandler("status", status_command))
    app.add_handler(CommandHandler("all", all_command))
    app.add_handler(CommandHandler("chains", chains_command))
    app.add_handler(CommandHandler("report", report_command))
    app.add_handler(CommandHandler('debug', debug_command))
    app.add_handler(CommandHandler('help', help_command))
    app.job_queue.run_repeating(job, interval=1800, first=5)  # Changed from 60 to 1800 seconds (30 minutes)
    app.run_polling(drop_pending_updates=True)

if __name__ == "__main__":
    start_bot()

from fastapi import FastAPI
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles

fastapi_app = FastAPI()

fastapi_app.mount("/static", StaticFiles(directory="."), name="static")

@fastapi_app.get("/dashboard")
async def get_dashboard():
    return FileResponse("dashboard.html")


@fastapi_app.get("/api/recs")
async def get_recs():
    pairs = await scan_market_all_async()
    return {"pairs": pairs}



async def debug_command(update, context: ContextTypes.DEFAULT_TYPE):
    pairs = await scan_market_all_async()
    lines = []
    for p in pairs[:30]:
        lines.append(f"{p['symbol']} | ${p['price']:.6f} | Δ {p['change']*100:.2f}%\n{p['token_address']}")
    text = "🐞 Debug Tokens:\n" + "\n\n".join(lines)
    await context.bot.send_message(chat_id=TELEGRAM_CHAT_ID, text=text)



async def help_command(update, context: ContextTypes.DEFAULT_TYPE):
    """List all available commands."""
    commands = [
        '/start', '/status', '/all', '/chains', '/report [daily|weekly|monthly]',
        '/ai_daily', '/debug', '/help'
    ]
    commands = [
        '/start', '/status', '/all', '/chains', '/report [daily|weekly|monthly]',
        '/ai_daily', '/debug', '/help'
    ]
    text = "📖 Available commands:\n" + "\n".join(commands)
    await context.bot.send_message(chat_id=TELEGRAM_CHAT_ID, text=text)

async def all_command(update, context: ContextTypes.DEFAULT_TYPE):
    pairs = await scan_market_all_async()
    lines = [f"{p['symbol']} ({p['change']*100:.2f}%) [{p['chain']}]" for p in pairs]
    text = "📋 All scanned pairs:\n" + "\n".join(lines[:50])
    await context.bot.send_message(chat_id=TELEGRAM_CHAT_ID, text=text)



async def debug_command(update, context: ContextTypes.DEFAULT_TYPE):
    pairs = await scan_market_all_async()
    lines = []
    for p in pairs[:30]:
        lines.append(f"{p['symbol']} | ${p['price']:.6f} | Δ {p['change']*100:.2f}%\n{p['token_address']}")
    text = "🐞 Debug Tokens:\n" + "\n\n".join(lines)
    await context.bot.send_message(chat_id=TELEGRAM_CHAT_ID, text=text)



async def all_command(update, context: ContextTypes.DEFAULT_TYPE):
    pairs = await scan_market_all_async()
    lines = []
    for p in pairs:
        chain = p.get("chain", "unknown")
        lines.append(f"{p['symbol']} ({p['change']*100:.2f}%) [{chain}]")
    text = "📋 All scanned pairs:\n" + "\n".join(lines[:50])
    await context.bot.send_message(chat_id=TELEGRAM_CHAT_ID, text=text)
