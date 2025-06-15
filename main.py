import asyncio

from payment_system.create_payment import create_payment


async def main():
    await create_payment(title="Заголовок платежа", price=100, order_number="12345")


if __name__ == "__main__":
    asyncio.run(main())