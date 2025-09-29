import unittest
from unittest.mock import patch, mock_open
import json
from scr.utils import load_operations, convert_valute

def test_valid_usd():
    tx = {'operationAmount': {'amount': '100', 'currency': {'code': 'USD'}}}
    assert convert_valute(tx) == (100.0, 'USD')

def test_missing_operationAmount():
    tx = {}
    assert convert_valute(tx) == 'Ошибка: подходящих операций не найдено'

def test_invalid_currency():
    tx = {'operationAmount': {'amount': '10', 'currency': {'code': 'RUB'}}}
    assert convert_valute(tx) == 'Ошибка: валюта не является USD или EUR'

def test_bad_structure():
    tx = {'operationAmount': 5}
    assert convert_valute(tx) == 'Ошибка: некорректная структура транзакции'

class TestLoadOperations(unittest.TestCase):

    @patch("builtins.open", new_callable=mock_open, read_data='[{"id":1},{"id":2}]')
    def test_load_valid_json_list(self, mock_file):
        # Тест с валидным JSON, который является списком
        result = load_operations("path")
        self.assertEqual(result, [{"id":1},{"id":2}])

    @patch("builtins.open", new_callable=mock_open, read_data='{"id":1}')
    def test_load_json_not_list(self, mock_file):
        # Тест, когда JSON не список
        result = load_operations("path")
        self.assertEqual(result, [])

    @patch("builtins.open", side_effect=FileNotFoundError)
    def test_file_not_found(self, mock_file):
        # Тест отсутствия файла
        result = load_operations("path")
        self.assertEqual(result, [])

    @patch("builtins.open", new_callable=mock_open, read_data='invalid json')
    def test_json_decode_error(self, mock_file):
        # Тест некорректного JSON
        result = load_operations("path")
        self.assertEqual(result, [])


