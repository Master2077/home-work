import json


def load_operations():
    try:
        # Читаем данные в operations.json
        with open("../data/operations.json", encoding="utf-8") as f:
            data = json.load(f)
        # Если в operations.json нет списка, то возвращаем пустой список
        if not isinstance(data, list):
            return []
        # Возвращаем данные из operations.json
        return data
    # Если файл operations.json не был обнаружен, то возвращаем пустой список
    except (FileNotFoundError, json.JSONDecodeError):
        return []


result_load_operations = load_operations()

# Вызов функции
print(result_load_operations)
