import pytest
import unittest
from unittest.mock import patch, MagicMock, AsyncMock
import json
from scr.external_api import convert_valute, api_convert, result_load_operations

def test_valid_usd():
    tx = {'operationAmount': {'amount': '100', 'currency': {'code': 'USD'}}}
    assert convert_valute.__wrapped__(tx) == (100.0, 'USD')

def test_missing_operationAmount():
    tx = {}
    assert convert_valute.__wrapped__(tx) == 'Ошибка: подходящих операций не найдено'

def test_invalid_currency():
    tx = {'operationAmount': {'amount': '10', 'currency': {'code': 'EUR'}}}
    assert convert_valute.__wrapped__(tx) == 'Ошибка: валюта не является USD или RUB'

def test_bad_structure():
    tx = {'operationAmount': 5}
    assert convert_valute.__wrapped__(tx) == 'Ошибка: некорректная структура транзакции'

