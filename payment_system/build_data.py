from enum import Enum

from payment_system.payment_config import TINKOFF_TERMINAL_KEY, SUCCESS_URL, EMAIL, PHONE_NUMBER
from payment_system.utils import generate_token


class VatType(Enum):
    NONE = "none" # — без НДС
    VAT0 = "vat0" # — НДС по ставке 0%
    VAT5 = "vat5" # — НДС по ставке 5%
    VAT7 = "vat7" # — НДС по ставке 7%
    VAT10 = "vat10" # — НДС чека по ставке 10%
    VAT20 = "vat20" # — НДС чека по ставке 20%
    VAT105 = "vat105" # — НДС чека по расчетной ставке 5/105
    VAT107 = "vat107" # — НДС чека по расчетной ставке 7/107
    VAT110 = "vat110" # — НДС чека по расчетной ставке 10/110
    VAT120 = "vat120" # — НДС чека по расчетной ставке 20/120


def build_payment_data(title: str, description: str, price: float, order_number: str, vat: VatType = VatType.NONE) -> dict:
    """
    Создает данные платежа.

    Amount указывается в копейках.
    По умолчанию используется умножение на 100, чтобы перевести рубли в копейки.

    Пример:
        price = 100 → Amount = 10000 копеек (100 рублей)
        price = 100.50 → int(100.50 * 100) = 10050 копеек (100 рублей 50 копеек)

    Если вы хотите работать с дробными ценами, убедитесь, что используете float корректно,
    или уберите (price * 100) из кода и передавайте сумму в копейках напрямую.
    """
    return {
        "TerminalKey": TINKOFF_TERMINAL_KEY,
        "Amount": int(price * 100),
        "OrderId": order_number,
        "Description": description,
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
                "Tax": vat.value,
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