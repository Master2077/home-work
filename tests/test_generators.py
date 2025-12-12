import pytest

from src.generators import card_number_generator, filter_by_currency, transaction_descriptions


# Фикстура с набором тестовых транзакций
@pytest.fixture
def sample_transactions():
    return [
        {"operationAmount": {"currency": {"code": "USD"}}, "id": 1},
        {"operationAmount": {"currency": {"code": "RUB"}}, "id": 2},
    ]


@pytest.mark.parametrize(
    "code, expected_ids",
    [
        ("USD", [1]),
        ("RUB", [2]),
    ],
)
def test_filter_by_existing_currency(sample_transactions, code, expected_ids):
    result = list(filter_by_currency(sample_transactions, code))
    assert [tx["id"] for tx in result] == expected_ids


def test_filter_by_invalid_currency(sample_transactions):
    # При неверном коде генератор выдаёт сообщения об ошибке
    result = list(filter_by_currency(sample_transactions, "duck"))
    assert result == ["Ошибка:", "Валюта не найдена"]


def test_filter_empty_list():
    # При пустом списке генератор выдаёт сообщения об ошибке
    result = list(filter_by_currency([], "USD"))
    assert result == ["Ошибка:", "Данные о валюте временно недоступны"]


@pytest.mark.parametrize(
    "transactions, expected",
    [
        # Одна полноценная транзакция
        ([{"description": "Оплата", "from": "A", "to": "B"}], ["Оплата", 'Перевод со "A" на "B"']),
        # Нет поля description
        ([{"description": "", "from": "X", "to": "Y"}], ["Ошибка:", "Описание операции не найдено"]),
        # Пустой список
        ([], ["Ошибка:", "Данные о операциях временно недоступны"]),
    ],
)
def test_transaction_descriptions_various(transactions, expected):
    result = list(transaction_descriptions(transactions))
    assert result == expected


@pytest.mark.parametrize(
    "start, stop, expected_lines",
    [
        (
            1,
            3,
            [
                "0000 0000 0000 0001",
                "0000 0000 0000 0002",
                "0000 0000 0000 0003",
            ],
        ),
        (
            9999999999999998,
            10000000000000000,
            [
                "9999 9999 9999 9998",
                "9999 9999 9999 9999",
                "1000 0000 0000 0000",
            ],
        ),
    ],
)
def test_card_number_generator_format_and_range(start, stop, expected_lines):
    result = list(card_number_generator(start, stop))
    assert result == expected_lines


def test_card_number_generator_empty_range(capsys):
    # Когда start > stop, ничего не печатается
    card_number_generator(5, 1)
    captured = capsys.readouterr().out
    assert captured == ""
