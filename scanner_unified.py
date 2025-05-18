
from scanner_gecko import scan_market_gecko
from scanner import scan_market as scan_market_dex
import logging

def scan_market():
    logging.info("🧪 Trying GeckoTerminal first...")
    results = scan_market_gecko()
    if results:
        logging.info("✅ Using GeckoTerminal results")
        return results

    logging.warning("⚠️ GeckoTerminal failed, falling back to Dexscreener...")
        logging.warning("⚠️ GeckoTerminal failed, falling back to Dexscreener...")
    return scan_market_dex()
