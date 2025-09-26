from functools import wraps
from os import getenv

import requests
from dotenv import load_dotenv

from scr.utils import result_load_operations

# Загружаем переменные окружения из .env
load_dotenv()


def api_convert(func):
    """
    Декоратор, который:
    - вызывает декорируемую функцию,
    - делает HTTPS-запрос к API конвертации валют,
    - возвращает строку с результатом в рублях или сообщение об ошибке.
    """

    @wraps(func)
    def wrapper(*args, **kwargs):
        try:
            result = func(*args, **kwargs)
            # Проверяем тип результата
            if isinstance(result, tuple):
                # Ожидаем, что result — кортеж (amount, code)
                amount, code = result
                # Формируем URL для запроса к apilayer
                url = f"https://api.apilayer.com/exchangerates_data/convert?to=RUB&from={code}&amount={amount}"
                # Получаем API-ключ из .env
                API_KEY = getenv("API_KEY")
                # Данные для GET запроса
                payload = {}
                headers = {"apikey": API_KEY}
                # GET запрос
                response = requests.request("GET", url, headers=headers, data=payload)
                # Текст ответа
                result = response.text
                # Если код ответа не 200 — возвращаем сообщение об ошибке с кодом статуса
                if response.status_code != 200:
                    return f"Ошибка API {response.status_code}"
                # Возвращаем ответ в рублях
                return f"В рублях: {result}"
            # Если result содержит (amount, code), то возвращаем его содержимое
            else:
                return result
        # Возвращаем ошибку в случае некорректной структуры транзакции
        except (TypeError, KeyError, ValueError):
            return "Ошибка: некорректная структура транзакции"

    return wrapper


@api_convert
def convert_valute(transactions):
    """
    Извлекает сумму и валюту из транзакции.

    Принимает словарь transactions, который должен содержать ключ operationAmount,
    внутри которого есть сумма (amount) и код валюты (code).

    Возвращает:
        - кортеж (amount, code), если всё получилось.
        - или сообщение об ошибке, если структура данных неправильная.
    """
    # Выводим текущую транзакцию для проверки
    print(f'Обрабатываем транзакцию: {transactions}')
    try:
        # Получаем operationAmount из транзакции
        op = transactions.get('operationAmount')
        # Если operationAmount нет, возвращаем ошибку
        if not op:
            return 'Ошибка: подходящих операций не найдено'
        # Возвращаем ошибку если валюта не является USD или RUB
        if op['currency']['code'] not in ('USD', 'RUB'):
            return 'Ошибка: валюта не является USD или RUB'
        # Выводим содержание operationAmount
        print(f'operationAmount: {op}')
        # Получаем код валюты
        code = op['currency']['code']
        # Получаем сумму и приводим ее к типу float
        amount = float(op['amount'])
        # Возвращаем сумму и валюту
        return amount, code
    # Ошибка при некорректной структуре транзакции
    except (TypeError, KeyError, ValueError) as e:
        return 'Ошибка: некорректная структура транзакции'

# Вызываем convert_valute и с помощью цикла по очереди вставляем в нее данные из result_load_operations
if __name__ == '__main__':
    for i in result_load_operations:
        print(convert_valute(i))
