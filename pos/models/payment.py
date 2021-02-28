from django.db import models

from people.models import People
from pos.models.pos import Shopping
from utilities.abstract_model import StatusModel, TimeStampedModel


class ChargeType(StatusModel):
    name = models.CharField(max_length=50)

    def __str__(self): return self.name


class Tax(StatusModel):
    amount = models.IntegerField()

    def __str__(self): return str(self.amount)


class PaymentType(StatusModel):
    name = models.CharField(max_length=50)

    def __str__(self): return self.name


class Payment(TimeStampedModel):
    people = models.ForeignKey(
        People, on_delete=models.PROTECT, null=True, blank=True
    )
    shopping = models.ForeignKey(
        Shopping, on_delete=models.PROTECT, null=True, blank=True
    )
    payment_type = models.ForeignKey(PaymentType, on_delete=models.PROTECT)
    amount = models.IntegerField()
    date = models.DateTimeField()
    note = models.TextField(null=True, blank=True)

    def __str__(self): return f'{self.people} Paid {self.amount}'
