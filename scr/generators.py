# Список словарей с данными транзакций
transactions = [
    {
        "id": 939719570,
        "state": "EXECUTED",
        "date": "2018-06-30T02:08:58.425572",
        "operationAmount": {"amount": "9824.07", "currency": {"name": "USD", "code": "USD"}},
        "description": "Перевод организации",
        "from": "Счет 75106830613657916952",
        "to": "Счет 11776614605963066702",
    },
    {
        "id": 142264268,
        "state": "EXECUTED",
        "date": "2019-04-04T23:20:05.206878",
        "operationAmount": {"amount": "79114.93", "currency": {"name": "USD", "code": "USD"}},
        "description": "Перевод со счета на счет",
        "from": "Счет 19708645243227258542",
        "to": "Счет 75651667383060284188",
    },
    {
        "id": 583920174,
        "state": "EXECUTED",
        "date": "2021-11-15T10:45:30.000000",
        "operationAmount": {"amount": "15000.00", "currency": {"name": "RUB", "code": "RUB"}},
        "description": "Покупка товаров в магазине",
        "from": "Счет 40817810099910004312",
        "to": "Счет 40817810900012345678",
    },
    {
        "id": 749302615,
        "state": "EXECUTED",
        "date": "2022-07-22T14:12:05.123456",
        "operationAmount": {"amount": "2500.50", "currency": {"name": "RUB", "code": "RUB"}},
        "description": "Оплата коммунальных услуг",
        "from": "Счет 40702810900000000001",
        "to": "Счет 40702810800000000002",
    },
]


def filter_by_currency(transactions, code):
    """
    Генератор, фильтрующий транзакции по коду валюты.
    Принимает список transactions и строку code ('USD' или 'RUB').
    """
    if transactions:
        if code in ("USD", "RUB"):  # проверка ввел ли пользователь корректную валюту
            for i in transactions:
                # если валюта совпадает – выводим транзакцию
                if i["operationAmount"]["currency"]["code"] == code:
                    yield i
        else:
            # при неправильном вводе выдаем сообщения об ошибке
            yield "Ошибка:"
            yield "Валюта не найдена"
    else:
        yield "Ошибка:"
        yield "Данные о валюте временно недоступны"


def transaction_descriptions(transactions):
    """
    Генератор который выводит описание транзакций
    и строку получателя и отправителя
    """
    if transactions:
        for i in transactions:
            if i.get("description"):
                # выводим текст описания операции
                yield i["description"]
            else:
                yield "Ошибка:"
                yield "Описание операции не найдено"
                continue

            if i.get("from") and i.get("to"):
                # выводим текст перевода между счетами
                yield f'Перевод со "{i["from"]}" на "{i["to"]}"'
    else:
        yield "Ошибка:"
        yield "Данные о операциях временно недоступны"


def card_number_generator(start, stop):
    """
    Функция печати номеров банковских карт в диапазоне от start до stop.
    Каждый номер 16-значный, группируется по четыре цифры.
    """

    stop += 1  # чтобы включить stop в диапазон
    card_number = "0000000000000000"  # шаблон карты
    for i in range(start, stop):  # перебираем числа
        s = str(i)  # переводим число(номер карты) в троку
        len_s = len(s)  # длина строки числа
        # обрезаем шаблон на длину числа и добавляем само число(номер карты)
        trimmed_card_number = card_number[:-len_s]
        # к обрезанному шаблону добавляем число(номер карты)
        result_card_number = trimmed_card_number + s
        # разбиваем на 4 части по 4 символа для правильного вида карты
        part1 = result_card_number[0:4]
        part2 = result_card_number[4:8]
        part3 = result_card_number[8:12]
        part4 = result_card_number[12:16]
        # выводим номер карты
        print(part1, part2, part3, part4)


if __name__ == "__main__":
    # запрос у пользователя кода валюты и приведение к верхнему регистру
    code = input("Введите название валюты USD/RUB: ").upper()
    # получаем генератор отфильтрованных транзакций
    usd_transactions = filter_by_currency(transactions, code)
    # выводим первые две подходящие транзакции
    for _ in range(2):
        print(next(usd_transactions))

    # получаем генератор описания транзакций
    descriptions = transaction_descriptions(transactions)
    # выводим первые 5 транзакций
    for _ in range(5):
        print(next(descriptions))

    # вызов генератора карты
    card_number_generator(1, 5)
print('')