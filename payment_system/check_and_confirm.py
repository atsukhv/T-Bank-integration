import asyncio

import aiohttp
from loguru import logger

from payment_system.build_data import build_getstate_data, build_confirm_data
from payment_system.utils import make_tinkoff_request


async def check_and_confirm_payment(payment_id: str):
    data = build_getstate_data(payment_id)

    async with aiohttp.ClientSession() as http_session:
        while True:
            response_data, status_code = await make_tinkoff_request(http_session, "https://securepay.tinkoff.ru/v2/GetState",  data)

            if status_code != 200:
                logger.error(f"№{payment_id}: Ошибка GetState: {response_data}, статус={status_code}")
                break

            status = response_data.get("Status", "UNKNOWN")

            if status == "CONFIRMED":
                logger.success(f"№{payment_id}: Платеж подтвержден. Статус: {status}")
                break

            elif status in ["CANCELED", "REJECTED"]:
                logger.error(f"№{payment_id}: Платеж отклонен. Статус: {status}")
                break

            elif status == "AUTHORIZED":
                await confirm_payment(payment_id)
                break

            await asyncio.sleep(10)


async def confirm_payment(payment_id: str, amount: int = None):
    data = build_confirm_data(payment_id, amount)

    async with aiohttp.ClientSession() as http_session:
        response_data, status_code = await make_tinkoff_request(http_session, "https://securepay.tinkoff.ru/v2/Confirm",  data)

    if status_code == 200 and response_data.get("Success"):
        logger.success(f"№{payment_id}: Платеж подтвержден. Статус: {response_data['Status']}")
    else:
        error_msg = response_data.get("Message", "Неизвестная ошибка")
        error_code = response_data.get("ErrorCode", "")
        logger.error(f"№{payment_id}: Ошибка подтверждения платежа. Код: {error_code}, Сообщение: {error_msg}")