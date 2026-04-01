import re

from collections import Counter

from src.info_transactions import result_csv, result_xlsx


search = 'EXECUTED'


def process_bank_search(data: list[dict], search: str) -> list[dict]:
    """
    Функция для отбора банковских операций по нужному статусу транзакции.
    """
    pattern = re.compile(search)
    result = [item for item in data if pattern.search(str(item))]
    return result


description = ['Перевод организации', 'Перевод с карты на карту', 'Перевод со счета на счет', 'Открытие вклада']


def process_bank_operations(data, description):
    """
    Функция для подсчета совпадающих элемнтов списка с строками файла
    """
    count_list = [d["description"] for d in data if d["description"] in description]
    return dict(Counter(count_list))


if __name__ == "__main__":
    a = process_bank_search(result_xlsx, search)
    print(a)
    b = process_bank_operations(result_xlsx, description)
    print(b)
