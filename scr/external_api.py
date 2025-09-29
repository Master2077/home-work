from os import getenv

import requests
from dotenv import load_dotenv

from scr.utils import convert_valute, result_load_operations

# Загружаем переменные окружения из .env
load_dotenv()


def api_convert(convert):
    """
    - вызывает декорируемую функцию,
    - делает HTTPS-запрос к API конвертации валют,
    - возвращает строку с результатом в рублях или сообщение об ошибке.
    """
    try:
        # Проверяем тип результата
        if isinstance(convert, tuple):
            # Ожидаем, что result — кортеж (amount, code)
            amount, code = convert
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
            result = response.json()
            # Если код ответа не 200 — возвращаем сообщение об ошибке с кодом статуса
            if response.status_code != 200:
                return f"Ошибка API {response.status_code}"
            # Возвращаем ответ в рублях
            return f"В рублях: {float(result)}"
        # Если result содержит (amount, code), то возвращаем его содержимое
        else:
            return convert
    # Возвращаем ошибку в случае некорректной структуры транзакции
    except (TypeError, KeyError, ValueError):
        return "Ошибка: некорректная структура транзакции"


convert_file = "../data/convert.txt"

# Вызываем convert_valute и с помощью цикла по очереди вставляем в нее данные из result_load_operations
if __name__ == "__main__":
    for transaction in result_load_operations:
        convert = convert_valute(transaction)
        with open(convert_file, "a", encoding="utf-8") as f:
            f.write(str(convert))
            f.write("\n")
