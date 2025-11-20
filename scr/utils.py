import json
import logging

success_logger = logging.getLogger("success_utils")
success_logger.setLevel(logging.DEBUG)
file_handler1 = logging.FileHandler("../logs/success_utils.log", "w", encoding="utf-8")
file_formatter1 = logging.Formatter("%(asctime)s - %(filename)s - %(levelname)s: %(message)s")
file_handler1.setFormatter(file_formatter1)
success_logger.addHandler(file_handler1)

errors_logger = logging.getLogger("errors_utils")
errors_logger.setLevel(logging.ERROR)
file_handler2 = logging.FileHandler("../logs/errors_utils.log", "w", encoding="utf-8")
file_formatter2 = logging.Formatter("%(asctime)s - %(filename)s - %(levelname)s: %(message)s")
file_handler2.setFormatter(file_formatter2)
errors_logger.addHandler(file_handler2)


# Переменная с указанием пути до json файла
path = "../data/operations.json"


def load_operations(path):
    try:
        # Читаем данные в operations.json
        success_logger.debug(f"Читаем данные в {path}")
        with open(path, encoding="utf-8") as f:
            data = json.load(f)
        # Если в operations.json нет списка, то возвращаем пустой список
        if not isinstance(data, list):
            success_logger.info(f"Получаем пустой список из {path}")
            return []
        # Возвращаем данные из operations.json
        success_logger.info(f"Возвращаем данные из {path}")
        return data
    # Если файл operations.json не был обнаружен, то возвращаем пустой список
    except (FileNotFoundError, json.JSONDecodeError):
        errors_logger.error(f"Файл {path} не обнаружен")
        return []


result_load_operations = load_operations(path)
