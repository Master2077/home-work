import json

# Переменная с указанием пути до json файла
path = "../data/operations.json"


def load_operations(path):
    try:
        # Читаем данные в operations.json
        with open(path, encoding="utf-8") as f:
            data = json.load(f)
        # Если в operations.json нет списка, то возвращаем пустой список
        if not isinstance(data, list):
            return []
        # Возвращаем данные из operations.json
        return data
    # Если файл operations.json не был обнаружен, то возвращаем пустой список
    except (FileNotFoundError, json.JSONDecodeError):
        return []


result_load_operations = load_operations(path)


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
        op = transactions.get("operationAmount")
        # Если operationAmount нет, возвращаем ошибку
        if not op:
            return "Ошибка: подходящих операций не найдено"
        # Возвращаем ошибку если валюта не является USD или RUB
        if op["currency"]["code"] not in ("USD", "EUR"):
            return "Ошибка: валюта не является USD или EUR"
        # Получаем код валюты
        code = op["currency"]["code"]
        # Получаем сумму и приводим ее к типу float
        amount = float(op["amount"])
        # Возвращаем сумму и валюту
        return amount, code
    # Ошибка при некорректной структуре транзакции
    except (TypeError, KeyError, ValueError) as e:
        return "Ошибка: некорректная структура транзакции"
