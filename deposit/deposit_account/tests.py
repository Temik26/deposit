import datetime

from dateutil.relativedelta import relativedelta
from django.test import TestCase
from django.urls import reverse
from parameterized import parameterized
from rest_framework import status
from rest_framework.test import APITestCase

from .business_logic.calculation import calculate_deposit, add_period_to_date


class DepositCalculationViewTest(APITestCase):
    def setUp(self) -> None:
        self.correct_input = {
            "date": "31.01.2021",
            "periods": 3,
            "amount": 10000,
            "rate": 6
        }
        self.correct_response = {
            '31.01.2021': 10050,
            '28.02.2021': 10100.25,
            '31.03.2021': 10150.75
        }
        self.incorrect_input = {
            "date": "xxxyyyy",
            "periods": 'rr',
            "amount": 500000000,
            "rate": 321
        }
        self.highest_allowed_amount = 3_000_000
        self.max_period = 60
        self.max_rate = 8
        self.correct_calculation = round(self.correct_input["amount"]
                                         * (1 + self.correct_input["rate"] / 12 / 100), 2)

    def test_send_valid_input_data(self):
        self.assertTrue(self.correct_input['periods'] <= self.max_period)
        self.assertTrue(self.correct_input['amount'] <= self.highest_allowed_amount)
        self.assertTrue(self.correct_input['rate'] <= self.max_rate)

    def test_correct_response(self):
        response = self.client.post(reverse("deposit_calculation"), self.correct_input)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(self.correct_response, response.json())

    def test_send_invalid_input_data(self):
        response = self.client.post(reverse("deposit_calculation"), self.incorrect_input)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_calculate_deposit_correctness(self):
        response = self.client.post(reverse("deposit_calculation"), self.correct_input)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data[self.correct_input["date"]], self.correct_calculation)
        self.assertEqual(len(response.data), self.correct_input["periods"])


class CalculationTest(TestCase):
    @parameterized.expand([
        ("2021-01-31", 3, 10_000, 6),
        ("2022-08-12", 12, 3_000_000, 8),
        ("2023-11-23", 12, 3_000_000, 8),
    ])
    def test_calculate_deposit(self, date, periods, amount, rate):
        result = calculate_deposit(date, periods, amount, rate)
        self.assertTrue(len(result) == periods)
        self.assertIsInstance(result, dict)
        self.assertIsInstance(date, str)
        self.assertIsInstance(periods, int)
        self.assertIsInstance(amount, int)
        self.assertIsInstance(rate, (int, float))

    @parameterized.expand([
        ("2021-01-31", 2),
        ("2021-08-30", 14),
        ("2023-12-30", 60),
        ("2025-12-30", 245),
    ])
    def test_add_period_to_date(self, date, period):
        result = add_period_to_date(date, period)
        deposit_date = datetime.datetime.strptime(date, '%Y-%m-%d')
        payment_date = datetime.datetime.strptime(result, '%d.%m.%Y')
        delta = relativedelta(payment_date, deposit_date)
        month_difference = delta.months + (delta.years * 12)
        self.assertIsInstance(result, str)
        self.assertEqual(period, month_difference)
        self.assertIsInstance(date, str)
        self.assertIsInstance(period, int)
