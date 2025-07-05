import pytest
from scr.masks import get_mask_card_number, get_mask_account


@pytest.mark.parametrize('inp, expected',
    [('123456789012345', '1234567890*2345'),
     ('0000000000000000000', '0000000000*****0000')]
)
def test_get_mask_card_number_valid(inp, expected):
    assert get_mask_card_number(inp) == expected

@pytest.mark.parametrize('inp', ['', '1234', 'abcd1234567890', '1234567890abcd'])
def test_get_mask_card_number_invalid(inp):
    assert get_mask_card_number(inp) == "Ошибка: Неправильный номер карты"

@pytest.mark.parametrize('inp, expected',
        [('123456', '**3456'),
         ('1234567890', '******7890')]
)
def test_get_mask_account_valid(inp, expected):
    assert get_mask_account(inp) == expected

@pytest.mark.parametrize('inp', ['', '123', '12ab34', '0000', '*23456'])
def test_get_mask_card_number_invalid(inp):
    assert get_mask_account(inp) == "Ошибка: Неправильный номер счета"



