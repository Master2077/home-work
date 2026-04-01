from src.masks import get_mask_account, get_mask_card_number  # Импортируем функции для маскирования данных


def mask_account_card(card_data: str) -> str:
    """
    Функция принимает строку с данными карты или счета, извлекает название
    и номер, маскирует номер карты, заменяя часть цифр на символы '*',
    и возвращает строку, состоящую из названия и замаскированного номера.
    """
    card_name_list: list = []  # Список для хранения символов названия карты
    account_name: str = ""  # Переменная для хранения названия карты или счета
    card_number_list: list = []  # Список для хранения цифр номера карты
    account_number: str = ""  # Переменная для хранения номера счета

    # Извлечение названия карты или счета
    for i in card_data:
        if i.isalpha() or i == " ":  # Проверяем, является ли символ буквой или пробелом
            card_name_list += i  # Добавляем символ в список названия
            account_name = "".join(card_name_list)  # Объединяем список в строку

    # Извлечение номера карты
    for i in card_data:

        if i.isdigit():  # Проверяем, является ли символ цифрой
            card_number_list += i  # Добавляем цифру в список номера карты
            account_number = "".join(card_number_list)  # Объединяем список в строку

    # Возвращаем название и замаскированный номер карты и счета
    if "Счет" not in account_name:
        return account_name + get_mask_card_number(account_number)  #
    else:
        return account_name + get_mask_account(account_number)


def get_date(time: str) -> str:
    """
    Функция принимает строку с датой и временем и возвращает строку,
    содержащую день, месяц и год в формате 'дд.мм.гггг'.
    """
    day: str = time[8:10]  # Извлекаем день из строки
    month: str = time[5:7]  # Извлекаем месяц из строки
    year: str = time[0:4]  # Извлекаем год из строки

    # Возвращаем дату в формате дд.мм.гггг'
    return day + "." + month + "." + year

if __name__ == '__main__':
    # Параметр содержащий номером карты
    # Активация функции mask_account_card
    card_data_number: str = "Master Card 1234567890123456"
    card_data_number_result: str = mask_account_card(card_data_number)
    print(card_data_number_result)

    # Параметр содержащий банковский счет
    # Активация функции mask_account_card
    card_data_account: str = "Счет 73654108430135874305"
    card_data_account_result: str = mask_account_card(card_data_account)
    print(card_data_account_result)

    # Параметр содержащий время
    # Активация функции get_date
    time: str = "2024-03-11T02:26:18.671407"
    time_result: str = get_date("2024-03-11T02:26:18.671407")
    print(time_result)
