from __future__ import annotations
from typing import Any, Dict, List, Tuple

# Исходные данные: список словарей с информацией о транзакциях
transactions: List[Dict[str, Any]] = [
    {"id": 41428829, "state": "EXECUTED", "date": "2019-07-03T18:35:29.512364"},
    {"id": 939719570, "state": "EXECUTED", "date": "2018-06-30T02:08:58.425572"},
    {"id": 594226727, "state": "CANCELED", "date": "2018-09-12T21:27:25.241689"},
    {"id": 615064591, "state": "CANCELED", "date": "2018-10-14T08:21:33.419441"},
]


def filter_by_state(transactions: List[Dict[str, Any]], state: str = "EXECUTED") -> List[Dict[str, Any]]:
    """
    Фильтрует и возвращает транзакции только с нужным состоянием.
    """
    card_status_information: List[Dict[str, Any]] = []  # Список для хранения выбранных отобранных транзакций
    two_state_options: Tuple[str, str] = ("EXECUTED", "CANCELED")  # Допустимые варианты состояния

    # Замена на EXECUTED, если пользователь указал неверные данные
    if state not in two_state_options:
        state = "EXECUTED"

    # Проходим по всем записям и добавляем в результат
    # только те, у которых state == выбранному
    for i in transactions:
        if i["state"] == state:
            card_status_information.append(i)
    return card_status_information


def sort_by_date(transactions: List[Dict[str, Any]], date: bool = False) -> List[Dict[str, Any]]:
    """
    Сортирует данные по дате транзакции (по убыванию)
    """

    def parse_date(date_str: str) -> int:
        """
        Преобразует строку даты в числовое значение для сортировки
        """
        date_part, time_part = date_str.split("T")  # Разделяем дату и время
        year, month, day = map(int, date_part.split("-"))  # Извлекаем год, месяц и день
        hour, minute, second = map(float, time_part.split(":"))  # Извлекаем часы, минуты и секунды

        # Преобразуем дату и время в одно целое число
        return year * 10000000000 + month * 100000000 + day * 1000000 + int(hour * 10000 + minute * 100 + second)

    # Сортируем данные по дате, используя функцию parse_date
    return sorted(transactions, key=lambda x: parse_date(x["date"]), reverse=date)

if __name__ == '__main__':
    # Вызов функции фильтрации и вывод результатов
    state_input: str = input("Введите состояние карты (EXECUTED или CANCELED:")
    result: List[Dict[str, Any]] = filter_by_state(transactions, state_input)
    print(result)  # Вывод списка выполненных транзакций

    # Вызов функции сортировки и вывод результатов
    sorted_data: List[Dict[str, Any]] = sort_by_date(transactions)
    print(sorted_data)  # Вывод отсортированных данных.
