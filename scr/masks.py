def get_mask_card_number(card_number: str) -> str:
    """
    Принимает номер карты в виде строки, проверяет его корректность и маскирует внутреннюю часть.

    Функция заменяет символы номера карты, начиная с 11-го символа до символа перед последними 4 символами,
    на символ '*'. Первые 10 символов и последние 4 остаются без изменений.
    """
    if card_number.isdigit() and len(card_number) > 14:

        # Преобразуем строку в список символов для возможности изменения элементов
        card_number_list: list[str] = list(card_number)

        # Заменяем символы с 10-го до предпоследних 4 на '*'
        for i in range(10, len(card_number) - 4):
            card_number_list[i] = "*"

        # Объединяем список обратно в строку
        return "".join(card_number_list)

    else:
        return "Ошибка: Неправильный номер карты"


def get_mask_account(mask_account: str) -> str:
    """
    Принимает номер счета в виде строки, проверяет его корректность и маскирует внутреннюю часть.

    Функция заменяет символы номера карты, начиная с 0-го символа до символа перед последними 4 символами,
    на символ '*'. Последние 4 символа  остаются без изменений.
    """
    if mask_account.isdigit() and len(mask_account) > 5:

        # Преобразуем строку в список символов для возможности изменения элементов
        mask_account_list: list[str] = list(mask_account)

        # Заменяем символы с 0-го до предпоследних 4 на '*'
        for i in range(0, len(mask_account_list) - 4):
            mask_account_list[i] = "*"

        # Объединяем список обратно в строку
        return "".join(mask_account_list)

    else:
        return "Ошибка: Неправильный номер счета"


if __name__ == "__main__":
    card_number: str = input("Введите номер карты: ")
    masked_number: str = get_mask_card_number(card_number)

    mask_account: str = input("Введите номер счета: ")
    masked_account: str = get_mask_account(mask_account)

    print(masked_number)
    print(masked_account)


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
print(sorted_data)  # Вывод отсортированных данных


