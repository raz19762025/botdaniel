import asyncio
import aiohttp
import logging

from settings import SCAN_LIMIT, PAGE_SIZE
from environment_manager import load_env_chain
from aiohttp import ClientResponseError

COINGECKO_MARKETS_URL = "https://api.coingecko.com/api/v3/coins/markets"

async def fetch_page(session, page: int):
    params = {
        "vs_currency": "usd",
        "order": "market_cap_desc",
        "per_page": PAGE_SIZE,
        "page": page,
        "sparkline": "false"
    }
    async with session.get(COINGECKO_MARKETS_URL, params=params) as resp:
        resp.raise_for_status()
        return await resp.json()

async def scan_market_all_async():
    """
    Asynchronously fetch up to SCAN_LIMIT assets,
    PAGE_SIZE per page, with throttle between requests.
    """
    results = []
    page = 1
    async with aiohttp.ClientSession() as session:
        while len(results) < SCAN_LIMIT:
            logging.debug(f"CoinGecko fetch page={page}")
            try:
                data = await fetch_page(session, page)
            except ClientResponseError as e:
                if e.status == 429:
                    logging.warning(f"Rate limited on page {page}, sleeping 60s")
                    await asyncio.sleep(60)
                    continue
                else:
                    raise
            if not data:
                break

            for item in data:
                token = {
                    "symbol": item.get("symbol", "").upper(),
                    "token_address": item.get("id"),
                    "price": float(item.get("current_price", 0) or 0),
                    "volume": float(item.get("total_volume", 0) or 0),
                    "liquidity": float(item.get("market_cap", 0) or 0),
                    "change": float(item.get("price_change_percentage_24h", 0) or 0) / 100,
                    "chain": load_env_chain()
                }
                results.append(token)
            page += 1

            # Throttle between pages to respect API limits
            await asyncio.sleep(1.3)

    return results[:SCAN_LIMIT]
