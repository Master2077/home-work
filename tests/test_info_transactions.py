import pytest
import pandas as pd
import unittest
from unittest import mock


from scr.info_transactions import transactions_csv, transactions_xlsx

class TestTransactions(unittest.TestCase):
    def data(self):
        self.df = pd.DataFrame([
            {'id': 1, 'from': 'A', 'to': 'B', 'amount': 666},
            {'id': 2, 'from': 'B', 'to': 'C', 'amount': 777},
        ])

    def test_transactions_csv_success(self):
        result = transactions_csv(self.df)
        expected = self.df.to_dict(orient='records')
        self.assertEqual(result, expected)

    def test_transactions_xlsx_success(self):
       result = transactions_xlsx(self.df)
       expected = self.df.to_dict(orient='records')
       self.assertEqual(result, expected)

    def test_transactions_csv_exception(self):
        bad = mock.MagicMock()
        bad.to_dict.side_effect = Exception("fail")
        result = transactions_csv(bad)
        self.assertEqual(result, "Данного файла не существует")

    def test_transactions_xlsx_exception(self):
        bad = mock.MagicMock()
        bad.to_dict.side_effect = Exception("fail")
        result = transactions_xlsx(bad)
        self.assertEqual(result, "Данного файла не существует")

