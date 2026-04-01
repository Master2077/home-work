import pytest

from collections import Counter

from src.search_transactions import process_bank_search, process_bank_operations


@pytest.fixture
def test_data():
    data = [
        {"status": "PENDING", "description": "Перевод организации"},
        {"status": "CANCELED", "description": "Перевод организации"},
        {"status": "PENDING", "description": "Перевод организации"},
        {"status": "EXECUTED", "description": "Перевод с карты на карту"},
    ]
    return data


@pytest.fixture
def test_search():
    return 'PENDING'


def test_process_bank_search(test_data, test_search):
    result = process_bank_search(test_data, test_search)
    assert len(result) == 2


@pytest.fixture
def test_description():
    return ['Перевод организации', 'Перевод с карты на карту', 'Перевод со счета на счет', 'Открытие вклада']


def test_process_bank_operations(test_data, test_description):
    result = process_bank_operations(test_data, test_description)
    assert dict(Counter(result))
