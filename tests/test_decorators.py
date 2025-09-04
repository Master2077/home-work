import pytest
import time
from scr.decorators import my_function

def test_my_function_zero_division(capsys):
    # Тестируем деление на 0
    my_function(10, 0)

    # Захватываем вывод
    captured = capsys.readouterr()

    # Проверяем, что вывод содержит ожидаемые строки
    assert "Функция: my_function" in captured.out
    assert "Ошибка: division by zero" in captured.out
    assert "Входные параметры:" in captured.out
    assert "Время выполнения:" in captured.out