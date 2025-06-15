import hashlib

import aiohttp
from loguru import logger
from payment_system.payment_config import TINKOFF_PASSWORD


def generate_token(data: dict) -> str:
    """Генерация токена по алгоритму Тинькофф."""
    token_data = {
        key: str(value)
        for key, value in data.items()
        if key not in ["Receipt", "DATA", "Shops"]
    }
    token_data["Password"] = TINKOFF_PASSWORD

    sorted_pairs = sorted(token_data.items())
    token_string = ''.join(val for _, val in sorted_pairs)

    return hashlib.sha256(token_string.encode('utf-8')).hexdigest()


async def make_tinkoff_request(session: aiohttp.ClientSession, url: str, data: dict):
    """Асинхронный запрос к API Тинькофф."""
    try:
        async with session.post(url, json=data, headers={'Content-Type': 'application/json'}) as response:
            return await response.json(), response.status
    except Exception as e:
        logger.error(f"Ошибка при запросе к {url}: {e}", exc_info=True)
        return {"error": str(e)}, 500