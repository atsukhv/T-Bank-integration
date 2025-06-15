# 💳 Python-модуль для работы с Tinkoff Pay

> Простая и чистая реализация взаимодействия с платежной системой **Tinkoff Pay (Tinkoff Касса)**. Подходит для интеграции в любые проекты: сайты, боты, приложения.

---

## 📌 Описание

Этот модуль предоставляет удобную асинхронную обёртку для работы с API **Tinkoff Pay**:
- Создание платежа
- Проверка статуса
- Подтверждение платежа

Реализован на **Python 3.10+** с использованием:
- `aiohttp` — для асинхронных HTTP-запросов
- `loguru` — для логирования
- `typing` — строгие типы

---

## ✅ Функционал

| Функция | Описание |
|--------|----------|
| `create_payment()` | Создает новый платеж и возвращает ссылку для оплаты |
| `check_and_confirm_payment()` | Периодически проверяет статус платежа |
| `confirm_payment()` | Подтверждает платеж (для двухстадийного платежа) |

---

## 🧩 Как использовать

### 1. Установи зависимости:

```bash
pip install aiohttp loguru
```

### 2. Настрой конфигурацию (payment_config.py):
```
TINKOFF_TERMINAL_KEY = 'ваш_терминал'
TINKOFF_PASSWORD = 'ваш_пароль'
SUCCESS_URL = 'https://вашсайт.com/success' 
EMAIL = 'email@example.com'
PHONE_NUMBER = '+79991234567'
```

### 3. Вызови создание платежа:
```
from payment_system.create_payment import create_payment
import asyncio

async def main():
    await create_payment(title="Оплата заказа", price=100, order_number="ORDER-001")

if __name__ == "__main__":
    asyncio.run(main())
```

### 📦build_payment_data()
Функция `build_payment_data()` формирует данные для создания платежа:
```python
def build_payment_data(title: str, price: float, order_number: str) -> dict:
    """
    Создает данные платежа.
    
    Amount указывается в копейках. 
    По умолчанию используется умножение на 100, чтобы перевести рубли в копейки.
    
    Пример:
        price = 100 → Amount = 10000 копеек (100 рублей)
        price = 100.50 → int(100.50 * 100) = 10050 копеек (100 рублей 50 копеек)
        
    Если вы хотите работать с дробными ценами, убедитесь, что используете float корректно,
    или передавайте сумму в копейках напрямую.
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
```

###⚠️ Важно: 
API Тинькофф принимает только целое число копеек.
Используйте float аккуратно, либо передавайте сумму сразу в копейках отдельным параметром.

### 📁 Структура проекта 
```
project/
├── main.py                  # Точка входа
└── payment_system/
    ├── build_data.py        # Формирование данных запроса
    ├── check_and_confirm.py # Проверка и подтверждение платежа
    ├── create_payment.py    # Инициация платежа
    ├── payment_config.py    # Конфигурация
    └── utils.py             # Вспомогательные функции (generate_token, make_tinkoff_request)
```

### 🔐 Генерация токена 

Токен генерируется автоматически по правилам Tinkoff: 

    - Все поля, кроме Receipt, DATA, Shops используются для генерации строки
    - Добавляется Password
    - Строка сортируется по ключам и хэшируется SHA256

### 📦 Преимущества этого решения 

    ✨ Чистый и понятный код
    ⚡ Асинхронная реализация (async/await)
    🧪 Легко расширяемая архитектура
    📋 Отдельные файлы для каждого типа запроса
    📜 Полностью документированный
    📎 Готов к интеграции в любой проект
     
     
### MIT License — используйте проект где угодно, меняйте и распространяйте. 

     
