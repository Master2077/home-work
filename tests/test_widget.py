import pytest
from scr.widget import mask_account_card, get_date

@pytest.mark.parametrize('inp, expected',
    [('Visa Platinum 7000792289606361', 'Visa Platinum 7000792289**6361'),
     ('Master Card 1234567890123456', 'Master Card 1234567890**3456'),]
)
def test_mask_account_card_card(inp, expected):
    """
        Проверяем для строк, которые не содержат 'Счет',
        должна сработать маскировка карты.
        """
    assert mask_account_card(inp) == expected

@pytest.mark.parametrize('inp, expected',
    [('Счет 73654108430135874305', 'Счет ****************4305'),
     ('Счет 430135874305', 'Счет ********4305')]
)
def test_mask_account_card_account(inp, expected):
    """
    Проверяем для строк, содержащих ключевое слово 'Счет',
    должна сработать маскировка счёта.
    """
    assert mask_account_card(inp) == expected

@pytest.mark.parametrize("iso_str, expected", [
    ("2024-03-11T02:26:18.671407", "11.03.2024"),
    ("1999-12-31T23:59:59.000000", "31.12.1999"),
    ("2020-01-01T00:00:00", "01.01.2020"),]
)
def test_get_date(iso_str, expected):
    assert get_date(iso_str) == expected

@pytest.mark.parametrize('inp', ['', 'dgdgdgdg'])
def test_mask_account_card_empty_or_malformed(inp):
    """
    Если вход пустой или не содержит цифр, mask_account_card вернёт name + error
    т.к. get_mask_* возвращает ошибку
    """
    assert mask_account_card(inp) == inp + "Ошибка: Неправильный номер карты"