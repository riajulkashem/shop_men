from django.db import models

from people.models import People
from product.models import Product
from user.models import User
from utilities.abstract_model import StatusModel, TimeStampedModel


class Shop(StatusModel):
    owner = models.ForeignKey(
        User, on_delete=models.PROTECT,
        related_name='shops'
    )
    name = models.CharField(max_length=200)
    logo = models.ImageField(
        upload_to='logo/', blank=True, null=True)
    store_bio = models.TextField(default='')
    address = models.TextField(default='')
    capital = models.IntegerField(default=0)
    cash_amount = models.IntegerField(default=0)
    admin_limit = models.IntegerField(default=1)
    staff_limit = models.IntegerField(default=0)

    def __str__(self): return self.name

    @property
    def current_cash(self):
        cash_in_total = sum(
            self.cash_in_history.values_list('amount', flat=True)
        )
        cash_out_total = sum(
            self.cash_in_history.values_list('amount', flat=True)
        )
        expanse_total = sum(
            self.expanse_history.values_list('amount', flat=True)
        )
        shopping_list = self.shoppings.all()
        cash_sale_total = sum(
            shopping_list.filter(
                people__people_type='customer'
            ).values_list('paid', flat=True)
        )
        cash_purchase_total = sum(
            shopping_list.filter(
                people__people_type='supplier'
            ).values_list('paid', flat=True)
        )
        total_income = cash_in_total + cash_sale_total
        total_expanse = cash_out_total + expanse_total + cash_purchase_total
        return total_income - total_expanse


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


class ChargeType(StatusModel):
    name = models.CharField(max_length=50)

    def __str__(self): return self.name


class Tax(StatusModel):
    amount = models.IntegerField()

    def __str__(self): return str(self.amount)


class PaymentType(StatusModel):
    name = models.CharField(max_length=50)

    def __str__(self): return self.name


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
    other_charge_type = models.ForeignKey(ChargeType, on_delete=models.PROTECT,
                                          null=True, blank=True)
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
