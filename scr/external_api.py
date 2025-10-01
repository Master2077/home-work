from os import getenv

import requests
from dotenv import load_dotenv

from scr.utils import result_load_operations

# Загружаем переменные окружения из .env
load_dotenv()


def convert_valute(transactions):
    """
    Извлекает сумму и валюту из транзакции.

    Принимает словарь transactions, который должен содержать ключ operationAmount,
    внутри которого есть сумма (amount) и код валюты (code).

    Возвращает:
        - кортеж (amount, code), если всё получилось.
        - или сообщение об ошибке, если структура данных неправильная.
    """
    try:
        # Получаем operationAmount из транзакции
        op = transactions.get('operationAmount')
        # Если operationAmount нет, возвращаем ошибку
        if not op:
            return 'Ошибка: подходящих операций не найдено'
        # Возвращаем ошибку если валюта не является USD, EUR или RUB
        if op['currency']['code'] not in ('USD', 'EUR', 'RUB'):
            return 'Ошибка: валюта не является USD или EUR'
        # Получаем код валюты
        code = op['currency']['code']
        # Получаем сумму и приводим ее к типу float
        amount = float(op['amount'])
        # Формируем URL для запроса к apilayer
        url = f"https://api.apilayer.com/exchangerates_data/convert?to=RUB&from={code}&amount={amount}"
        # Получаем API-ключ из .env
        API_KEY = getenv("API_KEY")
        # Проверка наличия API_KEY
        if not API_KEY:
            return "Ошибка: API_KEY не установлен"
        # Данные для GET запроса
        headers = {"apikey": API_KEY}
        # Выполняем GET-запрос
        response = requests.request("GET", url, headers=headers)
        # Если код ответа не 200 — возвращаем сообщение об ошибке с кодом статуса
        if response.status_code != 200:
            return f"Ошибка API {response.status_code}"
        # Текст ответа
        result = response.json()
        # Возвращаем результат конвертации
        return f"В рублях: {float(result)}"

    # Возвращаем ошибку в случае некорректной структуры транзакции
    except Exception as e:
        return "Ошибка: некорректная структура транзакции"

convert_file = "../data/convert.txt"

# С помощью цикла по очереди вставляем в нее данные из result_load_operations
if __name__ == "__main__":
    for transaction in result_load_operations:
        convert = convert_valute(transaction)
        with open(convert_file, "a", encoding="utf-8") as f:
            f.write(convert)
            f.write("\n")
