import json
import logging

logger = logging.getLogger("utils")
logger.setLevel(logging.DEBUG)
file_handler1 = logging.FileHandler("../logs/utils.log", "w", encoding="utf-8")
file_formatter1 = logging.Formatter("%(asctime)s - %(filename)s - %(levelname)s: %(message)s")
file_handler1.setFormatter(file_formatter1)
logger.addHandler(file_handler1)


# Переменная с указанием пути до json файла
path = "../data/operations.json"


def load_operations(path):
    try:
        # Читаем данные в operations.json
        logger.debug(f"Читаем данные в {path}")
        with open(path, encoding="utf-8") as f:
            data = json.load(f)
        # Если в operations.json нет списка, то возвращаем пустой список
        if not isinstance(data, list):
            logger.info(f"Получаем пустой список из {path}")
            return []
        # Возвращаем данные из operations.json
        logger.info(f"Возвращаем данные из {path}")
        return data
    # Если файл operations.json не был обнаружен, то возвращаем пустой список
    except (FileNotFoundError, json.JSONDecodeError):
        logger.error(f"Файл {path} не обнаружен")
        return []

result_load_operations = load_operations(path)
if __name__ == '__main__':
    print(result_load_operations)
