# Исходные данные: список словарей с информацией о транзакциях
data = [{'id': 41428829, 'state': 'EXECUTED', 'date': '2019-07-03T18:35:29.512364'},
        {'id': 939719570, 'state': 'EXECUTED', 'date': '2018-06-30T02:08:58.425572'},
        {'id': 594226727, 'state': 'CANCELED', 'date': '2018-09-12T21:27:25.241689'},
        {'id': 615064591, 'state': 'CANCELED', 'date': '2018-10-14T08:21:33.419441'}]

def filter_by_state(data: list[dict], state: str = 'EXECUTED') -> tuple[list[dict], list[dict]]:
    """
    Фильтрует данные по состоянию транзакции (EXECUTED и CANCELED)
    """
    data_executed = []   # Список для хранения транзакций с состоянием EXECUTED
    data_canceled = []   # Список для хранения транзакций с состоянием CANCELED

    for i in data:
        if i['state'] == state:
            data_executed.append(i) # Добавляем транзакцию в список выполненных
        elif i['state'] != state:
            data_canceled.append(i) # Добавляем транзакцию в список отмененных

    return data_executed, data_canceled # Возвращаем оба списка

# Вызов функции фильтрации и вывод результатов
result_executed, result_canceled = filter_by_state(data)
print(result_executed)  # Вывод списка выполненных транзакций
print(result_canceled)  # Вывод списка отмененных транзакци


def sort_by_date(data: list[dict], date: bool = True) -> list[dict]:
    """
    Сортирует данные по дате транзакции (по убыванию)
    """
    def parse_date(date_str: str) -> int:
        """
        Преобразует строку даты в числовое значение для сортировки
        """
        date_part, time_part = date_str.split('T')  # Разделяем дату и время
        year, month, day = map(int, date_part.split('-'))  # Извлекаем год, месяц и день
        hour, minute, second = map(float, time_part.split(':'))  # Извлекаем часы, минуты и секунды

        # Преобразуем дату и время в одно целое число
        return year * 10000000000 + month * 100000000 + day * 1000000 + int(hour * 10000 + minute * 100 + second)

    # Сортируем данные по дате, используя функцию parse_date
    return sorted(data, key=lambda x: parse_date(x['date']), reverse=date)

 # Вызов функции сортировки и вывод результатов
sorted_data = sort_by_date(data)
print(sorted_data)  # Вывод отсортированных данных.


