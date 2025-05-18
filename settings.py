import os
from dotenv import load_dotenv, find_dotenv
dotenv_path = find_dotenv()
print("📂 dotenv_path →", dotenv_path)
load_dotenv(dotenv_path, override=True)
from dotenv import load_dotenv

load_dotenv()

TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
TELEGRAM_CHAT_ID   = int(os.getenv("TELEGRAM_CHAT_ID", "0"))

BSC_RPC_URL        = os.getenv("BSC_RPC_URL")
BSC_PRIVATE_KEY    = os.getenv("BSC_PRIVATE_KEY")
WALLET_ADDRESS     = os.getenv("WALLET_ADDRESS")
BSC_CHAIN_ID       = int(os.getenv("BSC_CHAIN_ID", "56"))

WEB_UI_PORT        = int(os.getenv("WEB_UI_PORT", "8001"))
DEXSCREENER_URL    = os.getenv(
    "DEXSCREENER_URL",
    "https://api.dexscreener.com/latest/dex/pairs/binance-smart-chain"
    "https://api.dexscreener.io/latest/dex/pairs/binance-smart-chain"
)
SCAN_INTERVAL_SEC = int(os.getenv("SCAN_INTERVAL_SEC", 60))
SLIPPAGE = float(os.getenv("SLIPPAGE", 0.02))
PROFIT_THRESHOLD = float(os.getenv("PROFIT_THRESHOLD", 0.10))
STOP_LOSS_THRESHOLD = float(os.getenv("STOP_LOSS_THRESHOLD", 0.10))

# Trading cost and target settings
TRADING_FEE_RATE = 0.001  # 0.1%
SLIPPAGE_RATE = 0.0005  # 0.05%
DAILY_TARGET_NET = 0.30  # 30%

RPC_URL = os.getenv("RPC_URL")

PRIVATE_KEY = os.getenv("PRIVATE_KEY")

# Pagination settings



# Pagination settings
PAGE_SIZE = int(os.getenv('PAGE_SIZE', '250'))
SCAN_LIMIT = int(os.getenv('SCAN_LIMIT', '6000'))
