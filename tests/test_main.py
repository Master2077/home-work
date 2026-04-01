import pytest

from collections import defaultdict
from datetime import datetime

from src.search_transactions import process_bank_search


@pytest.fixture
def test_data_transactions():
    data_transactions = [
        {
            "id": 3226899,
            "state": "EXECUTED",
            "date": "2023-04-17T09:21:15Z",
            "amount": 21680,
            "currency_name": "Koruna",
            "currency_code": "CZK",
            "from": "",
            "to": "Счет 88329674734590848775",
            "description": "Открытие вклада",
        },
        {
            "id": 3176764,
            "state": "CANCELED",
            "date": "2022-08-24T14:32:38Z",
            "amount": 16652,
            "currency_name": "Euro",
            "currency_code": "EUR",
            "from": "Mastercard 8387037425051294",
            "to": "American Express 5556525473658852",
            "description": "Перевод с карты на карту",
        },
        {
            "id": 2130098,
            "state": "PENDING",
            "date": "2020-06-07T11:11:36Z",
            "amount": 30731,
            "currency_name": "руб.",
            "currency_code": "RUB",
            "from": "Visa 5749750597771353",
            "to": "American Express 9106381490184499",
            "description": "Перевод с карты на карту",
        },
        {
            "id": 2130093,
            "state": "PENDING",
            "date": "2020-05-07T11:11:36Z",
            "amount": 30731,
            "currency_name": "Euro",
            "currency_code": "EUR",
            "from": "Visa 5749750597771353",
            "to": "American Express 9106381490184499",
            "description": "Перевод с карты на карту",
        },
    ]
    return data_transactions


@pytest.fixture
def test_search():
    return "PENDING"


def test_file_filtering1(test_data_transactions, test_search):
    result = process_bank_search(test_data_transactions, test_search)
    assert len(result) == 2


@pytest.fixture
def filtered_status_transactions(test_data_transactions, test_search):
    """Возвращает только PENDING операции"""
    return process_bank_search(test_data_transactions, test_search)


def test_file_filtering3_ascending_order(filtered_status_transactions):
    groups = defaultdict(list)
    for item in filtered_status_transactions:
        date_str = item.get("date")
        groups[date_str].append(item)  # date_str может быть None — будет ключ None
    # отсортировать ключи, пропуская None
    sorted_dates = sorted((d for d in groups.keys() if d), key=lambda s: datetime.strptime(s, "%Y-%m-%dT%H:%M:%SZ"))

    filter_by_date = [op for d in sorted_dates for op in groups[d]]
    assert filter_by_date == [
        {
            "id": 2130093,
            "state": "PENDING",
            "date": "2020-05-07T11:11:36Z",
            "amount": 30731,
            "currency_name": "Euro",
            "currency_code": "EUR",
            "from": "Visa 5749750597771353",
            "to": "American Express 9106381490184499",
            "description": "Перевод с карты на карту",
        },
        {
            "id": 2130098,
            "state": "PENDING",
            "date": "2020-06-07T11:11:36Z",
            "amount": 30731,
            "currency_name": "руб.",
            "currency_code": "RUB",
            "from": "Visa 5749750597771353",
            "to": "American Express 9106381490184499",
            "description": "Перевод с карты на карту",
        },
    ]


def test_file_filtering3_descending_order(filtered_status_transactions):
    filter_by_date = sorted(
        filtered_status_transactions,
        key=lambda x: datetime.strptime(x["date"], "%Y-%m-%dT%H:%M:%SZ"),
        reverse=True,
    )
    assert filter_by_date == [
        {
            "id": 2130098,
            "state": "PENDING",
            "date": "2020-06-07T11:11:36Z",
            "amount": 30731,
            "currency_name": "руб.",
            "currency_code": "RUB",
            "from": "Visa 5749750597771353",
            "to": "American Express 9106381490184499",
            "description": "Перевод с карты на карту",
        },
        {
            "id": 2130093,
            "state": "PENDING",
            "date": "2020-05-07T11:11:36Z",
            "amount": 30731,
            "currency_name": "Euro",
            "currency_code": "EUR",
            "from": "Visa 5749750597771353",
            "to": "American Express 9106381490184499",
            "description": "Перевод с карты на карту",
        },
    ]


@pytest.fixture
def test_descending_order(filtered_status_transactions):
    filter_by_date = sorted(
        filtered_status_transactions,
        key=lambda x: datetime.strptime(x["date"], "%Y-%m-%dT%H:%M:%SZ"),
        reverse=True,
    )
    return filter_by_date


def test_file_filtering3_ruble_search(test_descending_order):
    filter_by_rub = process_bank_search(test_descending_order, "RUB")
    assert filter_by_rub == [
        {
            "id": 2130098,
            "state": "PENDING",
            "date": "2020-06-07T11:11:36Z",
            "amount": 30731,
            "currency_name": "руб.",
            "currency_code": "RUB",
            "from": "Visa 5749750597771353",
            "to": "American Express 9106381490184499",
            "description": "Перевод с карты на карту",
        }
    ]


@pytest.fixture
def test_ruble_search(test_descending_order):
    filter_by_rub = process_bank_search(test_descending_order, "RUB")
    return filter_by_rub


def test_file_filtering4_search_by_word(test_ruble_search):
    filter_by_word = process_bank_search(test_ruble_search, "Перевод с карты на карту")
    assert filter_by_word == [
        {
            "id": 2130098,
            "state": "PENDING",
            "date": "2020-06-07T11:11:36Z",
            "amount": 30731,
            "currency_name": "руб.",
            "currency_code": "RUB",
            "from": "Visa 5749750597771353",
            "to": "American Express 9106381490184499",
            "description": "Перевод с карты на карту",
        }
    ]
