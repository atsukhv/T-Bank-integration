import asyncio

from loguru import logger

import aiohttp

from payment_system.build_data import build_payment_data, VatType
from payment_system.check_and_confirm import check_and_confirm_payment
from payment_system.utils import generate_token, make_tinkoff_request


async def create_payment(title: str, description: str, price: float, order_number: str, vat: VatType):
    data = build_payment_data(title, description, price, order_number, vat)
    data["Token"] = generate_token(data)

    async with aiohttp.ClientSession() as http_session:
        response_data, status_code = await make_tinkoff_request(http_session, "https://securepay.tinkoff.ru/v2/Init",  data)

    if status_code == 200 and 'PaymentURL' in response_data:
        payment_url = response_data['PaymentURL']
        logger.info(f"№{response_data['PaymentId']}: Платеж создан. Статус: {response_data['Status']}, "
                    f"ссылка: {payment_url}")

        asyncio.create_task(check_and_confirm_payment(response_data['PaymentId']))
        return payment_url

    else:
        logger.error(f"Ошибка создания платежа: {response_data}, статус={status_code}")


async def test_create_payment():
    data = await create_payment(title="Заголовок платежа", description="Описание платежа", price=100.0, order_number="1234567890",
    vat=VatType.NONE)
    print("Платеж создан")
    print(data)


if __name__ == "__main__":
    asyncio.run(test_create_payment())
