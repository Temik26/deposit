import datetime
from dataclasses import dataclass

from dateutil.relativedelta import relativedelta


@dataclass
class DepositDetails:
    date: str
    periods: int
    amount: int
    rate: float


def add_period_to_date(date: str, period: int):
    date_object = datetime.datetime.strptime(date, "%Y-%m-%d").date()
    new_date = (date_object + relativedelta(months=period)).strftime('%d.%m.%Y')
    return new_date


def calculate_deposit(current_date: str, periods: int,
                      amount: int, rate: float):
    calculated_periods = {}
    for period in range(periods):
        date = add_period_to_date(current_date, period)
        if calculated_periods:
            previous_date = list(calculated_periods.keys())[-1]
            value_of_previous_date = calculated_periods[previous_date]
            calculated_periods[date] = round(value_of_previous_date * (1 + rate / 12 / 100), 2)
        else:
            calculated_periods[date] = round(amount * (1 + rate / 12 / 100), 2)
    return calculated_periods
