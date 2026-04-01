import pytest

from src.widget import get_date, mask_account_card


@pytest.mark.parametrize(
    ("inp", "expected"),
    [
        ("Visa Platinum 7000792289606361", "Visa Platinum 7000792289**6361"),
        ("Master Card 1234567890123456", "Master Card 1234567890**3456"),
    ],
)
def test_mask_account_card_card(inp: str, expected: str) -> None:
    """
    Проверяем строки без 'Счет' — должна сработать маскировка карты.
    """
    result: str = mask_account_card(inp)
    assert result == expected


@pytest.mark.parametrize(
    ("inp", "expected"),
    [
        ("Счет 73654108430135874305", "Счет ****************4305"),
        ("Счет 430135874305", "Счет ********4305"),
    ],
)
def test_mask_account_card_account(inp: str, expected: str) -> None:
    """
    Проверяем строки с 'Счет' — должна сработать маскировка счёта.
    """
    result: str = mask_account_card(inp)
    assert result == expected


@pytest.mark.parametrize(
    ("iso_str", "expected"),
    [
        ("2024-03-11T02:26:18.671407", "11.03.2024"),
        ("1999-12-31T23:59:59.000000", "31.12.1999"),
        ("2020-01-01T00:00:00", "01.01.2020"),
    ],
)
def test_get_date(iso_str: str, expected: str) -> None:
    """
    Проверяем преобразование ISO-строки в формат 'DD.MM.YYYY'.
    """
    result: str = get_date(iso_str)
    assert result == expected


@pytest.mark.parametrize(
    "inp",
    ["", "abcdef", "NoDigitsHere"],
)
def test_mask_account_card_empty_or_malformed(inp: str) -> None:
    """
    Если строка пустая или не содержит цифр — должна быть ошибка.
    mask_account_card прибавляет к исходной строке сообщение об ошибке.
    """
    result: str = mask_account_card(inp)
    # Ожидаем, что внутренняя логика выдаст сообщение о неверном номере карты
    assert result == inp + "Ошибка: Неправильный номер карты"
