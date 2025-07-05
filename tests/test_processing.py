from typing import Any, Dict, List

import pytest

from scr.processing import filter_by_state, sort_by_date

# фикстурные данные для тестирования
transactions: List[Dict[str, Any]] = [
    {"id": 41428829, "state": "EXECUTED", "date": "2019-07-03T18:35:29.512364"},
    {"id": 939719570, "state": "EXECUTED", "date": "2018-06-30T02:08:58.425572"},
    {"id": 594226727, "state": "CANCELED", "date": "2018-09-12T21:27:25.241689"},
    {"id": 615064591, "state": "CANCELED", "date": "2018-10-14T08:21:33.419441"},
]


@pytest.mark.parametrize(
    ("state", "expected_count"),
    [
        ("EXECUTED", 2),  # два EXECUTED
        ("CANCELED", 2),  # два CANCELED
        ("INVALID_STATE", 2),  # неверный → по умолчанию EXECUTED → 2
    ],
    ids=["executed", "canceled", "invalid"],
)
def test_filter_by_state(state: str, expected_count: int) -> None:
    """
    Проверяем, что filter_by_state возвращает корректное число записей
    и что при неверном ключе берётся EXECUTED.
    """
    result: List[Dict[str, Any]] = filter_by_state(transactions, state)
    assert len(result) == expected_count


@pytest.mark.parametrize(
    ("reverse", "expected_ids"),
    [
        # от самых старых к самым новым (reverse=False)
        (False, [939719570, 594226727, 615064591, 41428829]),
        # от самых новых к самым старым (reverse=True)
        (True, [41428829, 615064591, 594226727, 939719570]),
    ],
    ids=["asc", "desc"],
)
def test_sort_by_date(reverse: bool, expected_ids: List[int]) -> None:
    """
    Проверяем, что sort_by_date сортирует по дате корректно
    в обеих направлениях.
    """
    sorted_list: List[Dict[str, Any]] = sort_by_date(transactions, date=reverse)
    # сравниваем порядок id — это уникальный и компактный способ проверки
    assert [t["id"] for t in sorted_list] == expected_ids
