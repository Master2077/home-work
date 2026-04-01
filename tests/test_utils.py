import json
from unittest import mock


from src.utils import load_operations


def make_open(read_data):
    """
    Возвращает файл, читающий read_data.
    Используется для patch('builtins.open')
    """
    return mock.mock_open(read_data=read_data)


def test_load_valid_list_json_with_mock():
    """
    Проверка корректной работы функции (данные файла должны быть списком)
    """
    data = [{"id": 1, "name": "op1"}, {"id": 2}]
    mock_file = make_open(json.dumps(data, ensure_ascii=False))
    with mock.patch("builtins.open", mock_file):
        result = load_operations("path.json")
    assert result == data


def test_load_non_list_json_returns_empty_with_mock():
    """
    Проверка данных не являющихся списком
    """
    data = {"id": 1, "name": "op1"}
    mock_file = make_open(json.dumps(data, ensure_ascii=False))
    with mock.patch("builtins.open", mock_file):
        result = load_operations("path/json")
    assert result == []


def test_load_missing_file_returns_empty():
    """
    Проверка при несуществующем файле
    """
    with mock.patch("builtins.open", side_effect=FileNotFoundError):
        result = load_operations("nonexistent.json")
    assert result == []


def test_load_invalid_json_returns_empty():
    """
    Проверка при некорректном json файле
    """
    mock_file = make_open("{invalid json}")
    with mock.patch("builtins.open", mock_file):
        result = load_operations("path.json")
    assert result == []
