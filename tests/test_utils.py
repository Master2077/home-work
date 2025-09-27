import pytest
import unittest
from unittest.mock import patch, mock_open
import json
from scr.utils import load_operations


class TestLoadOperations(unittest.TestCase):

    @patch("builtins.open", new_callable=mock_open, read_data='[{"id": 1, "name": "Operation 1"}]')
    def test_valid_json_list(self, mock_file):
        # Правильный вариант возвращаюсь данные из файла json
        result = load_operations()
        self.assertEqual(result, [{"id": 1, "name": "Operation 1"}])
        mock_file.assert_called_once_with("../data/operations.json", encoding="utf-8")

    @patch("builtins.open", new_callable=mock_open, read_data='{"id": 1, "name": "Operation 1"}')
    def test_json_not_list(self, mock_file):
        # Cодержит словарь а не список
        result = load_operations()
        self.assertEqual(result, [])
        mock_file.assert_called_once_with("../data/operations.json", encoding="utf-8")

    @patch("builtins.open", side_effect=FileNotFoundError)
    def test_file_not_found(self, mock_file):
        # При отсутствии файла
        result = load_operations()
        self.assertEqual(result, [])
        mock_file.assert_called_once_with("../data/operations.json", encoding="utf-8")





