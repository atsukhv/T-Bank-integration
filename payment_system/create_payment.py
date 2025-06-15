import asyncio

from loguru import logger

import aiohttp

from payment_system.build_data import build_payment_data
from payment_system.check_and_confirm import check_and_confirm_payment
from payment_system.utils import generate_token, make_tinkoff_request


async def create_payment(title: str, price: float, order_number: str):
    data = build_payment_data(title, price, order_number)
    data["Token"] = generate_token(data)

    async with aiohttp.ClientSession() as http_session:
        response_data, status_code = await make_tinkoff_request(http_session, "https://securepay.tinkoff.ru/v2/Init",  data)

    if status_code == 200 and 'PaymentURL' in response_data:
        payment_url = response_data['PaymentURL']
        logger.info(f"№{response_data['PaymentId']}: Платеж создан. Статус: {response_data['Status']}, "
                    f"ссылка: {payment_url}")

        asyncio.create_task(check_and_confirm_payment(response_data['PaymentId']))

    else:
        logger.error(f"Ошибка создания платежа: {response_data}, статус={status_code}")


async def main():
    await create_payment(title="Заголовок платежа", price=100, order_number="12345")


if __name__ == "__main__":
    asyncio.run(main())
