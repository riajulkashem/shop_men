from django.db import models

from pos.models import Shop
from utilities.abstract_model import TimeStampedModel


class CashIn(TimeStampedModel):
    shop = models.ForeignKey(
        Shop,
        verbose_name="Shop",
        on_delete=models.PROTECT,
        related_name="cash_in_history"
    )
    amount = models.BigIntegerField()
    note = models.TextField(null=True, blank=True)
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Cash In {self.amount}'


class CashOut(TimeStampedModel):
    shop = models.ForeignKey(
        Shop,
        verbose_name="Shop",
        on_delete=models.PROTECT,
        related_name="cash_out_history"
    )
    amount = models.BigIntegerField()
    note = models.TextField(null=True, blank=True)
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Cash Out {self.amount}'


class Expanse(TimeStampedModel):
    shop = models.ForeignKey(
        Shop,
        verbose_name="Shop",
        on_delete=models.PROTECT,
        related_name="expanse_history"
    )
    amount = models.BigIntegerField()
    date = models.DateTimeField(auto_now_add=True)
    note = models.TextField()

    def __str__(self):
        return f'Cash Out {self.amount}'

