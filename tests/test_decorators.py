import pytest

from scr.decorators import log, my_function

LOG_FILE = "mylog.txt"


@log(filename=LOG_FILE)
def test_my_function_zero_division_txt():
    # Тестируем деление на 0 в mylog.txt
    def my_function(x, y):
        return x / y

    my_function(10, 0)


with open(LOG_FILE, "r", encoding="utf-8") as file:
    log_content = file.read()

    assert "Функция: my_function" in log_content
    assert "Ошибка: division by zero" in log_content
    assert "Входные параметры:" in log_content
    assert "Время выполнения:" in log_content


@log(filename=LOG_FILE)
def test_my_function_valid_txt():
    # Тестируем деление на 2 в mylog.txt
    def my_function(x, y):
        return x / y

    my_function(10, 2)


with open(LOG_FILE, "r", encoding="utf-8") as file:
    log_content = file.read()

    assert "Функция: my_function" in log_content
    assert "Входные параметры:" in log_content
    assert "Время выполнения:" in log_content


@log(filename=None)
def test_my_function_zero_division_consol(capsys):
    # Тестируем деление на 0 в консоли
    def my_function(x, y):
        return x / y

    my_function(0, 0)

    captured = capsys.readouterr()

    # Проверяем, что вывод содержит ожидаемые строки
    assert "Функция: my_function" in captured.out
    assert "Ошибка: division by zero" in captured.out
    assert "Входные параметры:" in captured.out
    assert "Время выполнения:" in captured.out


@log(filename=None)
def test_my_function_valid_consol(capsys):
    # Тестируем деление на 2 в консоли
    def my_function(x, y):
        return x / y

    my_function(10, 2)

    captured = capsys.readouterr()

    # Проверяем, что вывод содержит ожидаемые строки
    assert "Функция: my_function" in captured.out
    assert "Результат: 5.0" in captured.out
    assert "Время выполнения:" in captured.out
