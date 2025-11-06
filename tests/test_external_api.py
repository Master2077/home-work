import unittest
from unittest import mock
from unittest.mock import Mock, patch

import pytest

from scr.external_api import convert_valute
from scr.utils import result_load_operations


@pytest.fixture
def valid_transaction():
    VALID_TRANSACTION = {
        "id": 441945886,
        "state": "EXECUTED",
        "date": "2019-08-26T10:50:58.294041",
        "operationAmount": {"amount": "31957.58", "currency": {"name": "руб.", "code": "RUB"}},
    }
    return VALID_TRANSACTION


@pytest.fixture
def invalid_transaction():
    INVALID_TRANSACTION = [
        {
            "id": 441945886,
            "state": "EXECUTED",
            "date": "2019-08-26T10:50:58.294041",
            "operationAmount": {"amount": "31957.58", "currency": {"name": "руб.", "code": "RUB"}},
        }
    ]
    return INVALID_TRANSACTION


@pytest.fixture
def invalid_not_operationamount_transaction():
    INVALID_TRANSACTION = {"id": 441945886, "state": "EXECUTED", "date": "2019-08-26T10:50:58.294041"}
    return INVALID_TRANSACTION


@pytest.fixture
def invalid_currency_transaction():
    INVALID_CURRENCY_TRANSACTION = {
        "id": 441945886,
        "state": "EXECUTED",
        "date": "2019-08-26T10:50:58.294041",
        "operationAmount": {"amount": "31957.58", "currency": {"name": "биткоин.", "code": "BTC"}},
    }
    return INVALID_CURRENCY_TRANSACTION


def test_valid_transaction(valid_transaction):
    assert convert_valute(valid_transaction) == 31957.58


def test_invalid_not_operationamount_transaction(invalid_not_operationamount_transaction):
    assert convert_valute(invalid_not_operationamount_transaction) == "Ошибка: подходящих операций не найдено"


def test_invalid_currency_transaction(invalid_currency_transaction):
    assert convert_valute(invalid_currency_transaction) == "Ошибка: валюта не является USD, EUR или RUB"


def test_invalid_transaction(invalid_transaction):
    assert convert_valute(invalid_transaction) == "Ошибка: некорректная структура транзакции"


def test_no_api_key(monkeypatch, valid_transaction):
    monkeypatch.delenv("API_KEY", raising=False)
    result = convert_valute(valid_transaction)
    assert result == "Ошибка: API_KEY не установлен"


@mock.patch("scr.external_api.requests.request")
def test_call_api_error(mock_request, valid_transaction):
    mock_response = Mock()
    mock_response.status_code = 500
    mock_request.return_value = mock_response
    result = convert_valute(valid_transaction)
    assert result == "Ошибка API 500"
