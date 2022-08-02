from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator


class Deposit(models.Model):
    date = models.DateField(verbose_name='Дата заявки')
    periods = models.IntegerField(verbose_name='Количество месяцев по вкладу',
                                  validators=[
                                      MinValueValidator(1),
                                      MaxValueValidator(60)])
    amount = models.IntegerField(verbose_name='Сумма вклада',
                                 validators=[
                                     MinValueValidator(10_000),
                                     MaxValueValidator(3_000_000)])
    rate = models.FloatField(verbose_name='Процент по вкладу',
                             validators=[
                                 MinValueValidator(1),
                                 MaxValueValidator(8)])
