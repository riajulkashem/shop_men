from django.db import models

from people.models import People
from pos.models import Shop
from pos.models.payment import PaymentType, Tax, ChargeType
from product.models import Product
from utilities.abstract_model import StatusModel, TimeStampedModel


class Shopping(StatusModel):
    SALE = (
        ('final', 'Final'),
        ('quotation', 'Quotation'),
    )
    DISCOUNT = (
        ('percentage', 'Percentage'),
        ('fixed', 'Fixed'),
    )

    PURCHASE = (
        ('received', 'Received'),
        ('pending', 'Pending'),
        ('ordered', 'Ordered'),
    )

    STATUS = (
        ('paid', 'PAID'),
        ('partial', 'PARTIAL'),
        ('due', 'DUE'),
    )
    shop = models.ForeignKey(
        Shop, on_delete=models.PROTECT,
        related_name='shoppings'
    )
    people = models.ForeignKey(
        People, on_delete=models.PROTECT, related_name='shoppings'
    )
    sale_status = models.CharField(max_length=50, choices=SALE, null=True)
    status = models.CharField(max_length=50, choices=STATUS, null=True)
    purchase_status = models.CharField(max_length=50, choices=PURCHASE,
                                       null=True)
    quantity = models.IntegerField()
    other_charge_type = models.ForeignKey(
        ChargeType, on_delete=models.PROTECT,
        null=True, blank=True
    )
    other_charge = models.FloatField(null=True, blank=True)
    paid = models.FloatField(null=True, blank=True)
    due = models.FloatField(null=True, blank=True)
    charge_total = models.FloatField(null=True, blank=True)
    discount_total = models.FloatField(null=True, blank=True)
    sub_total = models.FloatField(null=True, blank=True)
    grand_total = models.FloatField(null=True, blank=True)
    discount = models.IntegerField(null=True, blank=True)
    discount_type = models.CharField(max_length=50, null=True, blank=True,
                                     choices=DISCOUNT)
    note = models.TextField(null=True, blank=True)
    date = models.DateTimeField()
    reference = models.CharField(max_length=100, null=True, blank=True)
    payment_type = models.ForeignKey(
        PaymentType, on_delete=models.PROTECT,
        null=True
    )

    def __str__(self):
        if self.sale_status is not None:
            return f'Sale Amount {self.grand_total}'
        return f'Purchase Amount {self.grand_total}'

    @property
    def shopping_id(self):
        return f'SL{self.created.date().strftime("%Y%m%d")}' \
               f'P{self.people_id}RK{self.id}'


class ShopItem(TimeStampedModel):
    DISCOUNT = (
        ('percentage', 'Percentage'),
        ('fixed', 'Fixed'),
    )
    TAX_TYPE = (
        ('inclusive', 'Inclusive'),
        ('exclusive', 'Exclusive'),
    )
    product = models.ForeignKey(Product, on_delete=models.PROTECT)
    quantity = models.IntegerField()
    price = models.FloatField()
    total = models.FloatField()
    tax_type = models.CharField(
        max_length=20,
        choices=TAX_TYPE,
        null=True,
        blank=True
    )
    tax = models.ForeignKey(
        Tax,
        on_delete=models.PROTECT,
        related_name='shopping_products',
        null=True,
        blank=True
    )
    shopping = models.ForeignKey(Shopping, on_delete=models.PROTECT,
                                 related_name='shopping_products')

    def __str__(self):
        return f'Product {self.product} Shop Id {self.shopping_id}'
