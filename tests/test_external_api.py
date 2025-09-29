from http.client import responses

import pytest
import unittest
from unittest.mock import patch, MagicMock, AsyncMock
import json
from scr.external_api import convert_valute, api_convert, result_load_operations

class ApiCobert():
    @patch('requests.request')
    def test_api_convert(mock_get):
        mock_get.return_value.json.return_value = (100, 'USD')
        code = 'USD'
        amount = 100

        assert api_convert('currency') == 10000
        mock_get.assert_called_once_with(f'https://api.apilayer.com/exchangerates_data/convert?to=RUB&from={code}&amount={amount}')

