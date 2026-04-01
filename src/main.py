import json
import time
from collections import defaultdict
from datetime import datetime

from src.info_transactions import result_csv, result_xlsx
from src.search_transactions import process_bank_search
from src.widget import get_date, mask_account_card


# Загрузка и проверка JSON файла
try:
    with open("../data/operations.json", encoding="utf-8") as f:
        data_json = json.load(f)
except FileNotFoundError:
    data_json = "Файла не существует"
except json.decoder.JSONDecodeError:
    data_json = "Файл пуст"
except Exception as e_json:
    data_json = f"Ошибка: {e_json}"


def main():
    """
    Основная функция программы.
    Реализует пошаговый интерактивный фильтр банковских операций.
    """
    print("Привет! Добро пожаловать в программу работы с банковскими транзакциями.")
    # Инициализация переменных-фильтров (каждый следующий фильтр применяется к результату предыдущего)
    format_file = None
    filter_by_status = None
    filter_by_date = None
    filter_by_rub = None
    filter_by_word = None

    # Выбор источника данных
    while True:
        file_of_interest = input(
            "Выберите необходимый пункт в меню:\n"
            "1. Получить информацию о транзакциях из JSON-файла\n"
            "2. Получить информацию о транзакциях из CSV-файла\n"
            "3. Получить информацию о транзакциях из XLSX-файла\n"
        )
        if file_of_interest == "1":
            format_file = data_json
            print("Для обработки выбран JSON-файл.")
            break
        if file_of_interest == "2":
            format_file = result_csv
            print("Для обработки выбран CSV-файл.")
            break
        if file_of_interest == "3":
            format_file = result_xlsx
            print("Для обработки выбран XLSX-файл.")
            break
        print("Данный пункт в меню отсутствует.")

    # Фильтрация по статусу операции
    while True:
        file_filtering1 = input(
            "Введите статус, по которому необходимо выполнить фильтрацию.\n"
            "Доступные для фильтровки статусы: EXECUTED, CANCELED, PENDING\n"
        )
        if file_filtering1.upper() in ("EXECUTED", "CANCELED", "PENDING"):
            filter_by_status = process_bank_search(format_file, file_filtering1.upper())
            print(f'Операции отфильтрованы по статусу "{file_filtering1}"')
            break
        print(f'Статус операции "{file_filtering1}" не доступен')

    # Сортировка по дате (опционально)
    while True:
        file_filtering2 = input("Отсортировать операции по дате? Да/Нет\n")
        if file_filtering2.lower() == "да":
            # Выполняем сортировку по дате при выборе "да"
            file_filtering3 = input("Отсортировать по возрастанию или по убыванию?\n")
            try:
                # Сортировка по возрастанию
                if file_filtering3.lower() == "по возрастанию":
                    if format_file == data_json:
                        groups = defaultdict(list)
                        for item in filter_by_status:
                            date_str = item.get("date")
                            groups[date_str].append(item)
                        sorted_dates = sorted(
                            (d for d in groups.keys() if d),
                            key=lambda s: datetime.strptime(s, "%Y-%m-%dT%H:%M:%S.%f")
                        )

                        filter_by_date = [op for d in sorted_dates for op in groups[d]]

                    if format_file == result_xlsx:
                        groups = defaultdict(list)
                        for item in filter_by_status:
                            date_str = item.get("date")
                            groups[date_str].append(item)
                        sorted_dates = sorted(
                            (d for d in groups.keys() if d),
                            key=lambda s: datetime.strptime(s, "%Y-%m-%dT%H:%M:%SZ")
                        )

                        filter_by_date = [op for d in sorted_dates for op in groups[d]]

                    if format_file == result_csv:
                        sorted_transactions = []
                        for entry in filter_by_status:
                            fields = entry[
                                "id;state;date;amount;currency_name;currency_code;from;to;description"
                            ].split(";")
                            transaction = dict(
                                zip(
                                    [
                                        "id",
                                        "state",
                                        "date",
                                        "amount",
                                        "currency_name",
                                        "currency_code",
                                        "from",
                                        "to",
                                        "description",
                                    ],
                                    fields,
                                )
                            )
                            sorted_transactions.append(transaction)
                        filter_by_date = sorted(
                            sorted_transactions,
                            key=lambda x: datetime.strptime(x["date"], "%Y-%m-%dT%H:%M:%SZ"),
                            reverse=False,
                        )
                    break

                # Сортировка по убыванию
                elif file_filtering3.lower() == "по убыванию":
                    if format_file == data_json:
                        filter_by_date = sorted(
                            filter_by_status,
                            key=lambda x: datetime.strptime(x["date"], "%Y-%m-%dT%H:%M:%S.%f"),
                            reverse=True,
                        )
                    if format_file == result_xlsx:
                        filter_by_date = sorted(
                            filter_by_status,
                            key=lambda x: datetime.strptime(x["date"], "%Y-%m-%dT%H:%M:%SZ"),
                            reverse=True,
                        )
                    if format_file == result_csv:
                        sorted_transactions = []
                        for entry in filter_by_status:
                            fields = entry[
                                "id;state;date;amount;currency_name;currency_code;from;to;description"
                            ].split(";")
                            transaction = dict(
                                zip(
                                    [
                                        "id",
                                        "state",
                                        "date",
                                        "amount",
                                        "currency_name",
                                        "currency_code",
                                        "from",
                                        "to",
                                        "description",
                                    ],
                                    fields,
                                )
                            )
                            sorted_transactions.append(transaction)
                        filter_by_date = sorted(
                            sorted_transactions,
                            key=lambda x: datetime.strptime(x["date"], "%Y-%m-%dT%H:%M:%SZ"),
                            reverse=True,
                        )
                    break
            except Exception:
                return "Ошибка: файл с транзакциями не верно структурирован"

        elif file_filtering2.lower() == "нет":
            try:
                if format_file == result_csv:
                    sorted_transactions = []
                    for entry in filter_by_status:
                        fields = entry[
                            "id;state;date;amount;currency_name;currency_code;from;to;description"
                        ].split(";")
                        transaction = dict(
                            zip(
                                [
                                    "id",
                                    "state",
                                    "date",
                                    "amount",
                                    "currency_name",
                                    "currency_code",
                                    "from",
                                    "to",
                                    "description",
                                ],
                                fields,
                            )
                        )
                        sorted_transactions.append(transaction)
                    filter_by_date = sorted_transactions
                else:
                    filter_by_date = filter_by_status
                break
            except Exception:
                return "Ошибка: файл с транзакциями не верно структурирован"

    # Фильтрация по рублевым транзакциям (опционально)
    while True:
        try:
            file_filtering3 = input("Выводить только рублевые транзакции? Да/Нет\n")
            if file_filtering3.lower() == "да":
                if format_file == data_json:
                    filter_by_rub = [
                        item
                        for item in data_json
                        if item.get("operationAmount", {}).get("currency", {}).get("code") == "RUB"
                    ]
                    break
                else:
                    filter_by_rub = process_bank_search(filter_by_date, "RUB")
                    break
            elif file_filtering3.lower() == "нет":
                filter_by_rub = filter_by_date
                break
        except Exception:
            return "Ошибка: файл с транзакциями не верно структурирован"

    # Фильтр по ключевому слову в описании (опционально)
    while True:
        file_filtering4 = input("Отфильтровать список транзакций по определенному слову в описании? Да/Нет\n")
        if file_filtering4.lower() == "да":
            certain_word = input("Напишите слово: \n")
            filter_by_word = process_bank_search(filter_by_rub, certain_word)
            break
        elif file_filtering4.lower() == "нет":
            filter_by_word = filter_by_rub
            break

    # Вывод результатов
    print("Распечатываю итоговый список транзакций...")
    time.sleep(3)
    total_operatios = len([item for item in filter_by_word])
    print(f"Всего банковских операций в выборке: {total_operatios}")
    if total_operatios == 0:
        print("Программа: Не найдено ни одной транзакции, подходящей под ваши условия фильтрации")

    for i in filter_by_word:
        if format_file == data_json:
            if i.get("date"):
                print(f"{get_date(i['date'])}")
            if i.get("operationAmount", {}).get("amount") and i.get("operationAmount", {}).get("currency", {}).get("code"):
                amount = i.get("operationAmount", {}).get("amount")
                code = i.get("operationAmount", {}).get("currency", {}).get("code")
                print(f"Сумма: {amount} {code}")
            print()

        if format_file == result_xlsx or format_file == result_csv:
            if i.get("date") and i.get("description"):
                print(f"{get_date(i['date'])} {i['description']}")
            if i.get("from"):
                if i.get("to"):
                    print(f"{mask_account_card(str(i['from']))} -> {mask_account_card(str(i['to']))}")
                else:
                    print(f"{mask_account_card(str(i['from']))}")
            if i.get("amount") and i.get("currency_code"):
                print(f"Сумма: {i['amount']} {i['currency_code']}")
            print()


main()