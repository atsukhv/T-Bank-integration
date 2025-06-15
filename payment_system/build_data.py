from payment_system.payment_config import TINKOFF_TERMINAL_KEY, SUCCESS_URL, EMAIL, PHONE_NUMBER
from payment_system.utils import generate_token

def build_payment_data(title: str, price: float, order_number: str) -> dict:
    """
    Создает данные платежа.
    Amount в рублях без копеек. Если нужны копейки убираем умножениее на 100.
    В таком случае в запросе указываем ещё и копейки, то есть 100руб - 10000
    """
    return {
        "TerminalKey": TINKOFF_TERMINAL_KEY,
        "Amount": int(price * 100),
        "OrderId": order_number,
        "Description": title,
        "SuccessURL": SUCCESS_URL,
        "PayType": 'O',
        "DATA": {"Phone": "", "Email": ""},
        "Receipt": {
            "Email": EMAIL,
            "Phone": PHONE_NUMBER,
            "Taxation": "osn",
            "Items": [{
                "Name": title,
                "Price": int(price * 100),
                "Quantity": 1,
                "Amount": int(price * 100),
                "Tax": "vat10",
            }]
        }
    }


def build_getstate_data(payment_id: str) -> dict:
    """Создает данные для проверки статуса платежа."""
    data = {
        "TerminalKey": TINKOFF_TERMINAL_KEY,
        "PaymentId": payment_id
    }
    data["Token"] = generate_token(data)
    return data


def build_confirm_data(payment_id: str, amount: int = None) -> dict:
    """Создает данные для подтверждения платежа."""
    data = {
        "TerminalKey": TINKOFF_TERMINAL_KEY,
        "PaymentId": payment_id,
        "IP": "192.168.255.255"
    }
    if amount is not None:
        data["Amount"] = amount
    data["Token"] = generate_token(data)
    return data