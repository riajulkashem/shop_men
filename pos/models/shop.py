from django.db import models

from user.models import User
from utilities.abstract_model import StatusModel
from datetime import datetime


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
    capital = models.IntegerField(
        default=0,
        verbose_name='Opening Balance',
        help_text='current cash which will be counted as cash amount'
    )
    cash_amount = models.IntegerField(default=0)
    admin_limit = models.IntegerField(default=1)
    staff_limit = models.IntegerField(default=0)

    def __str__(self): return self.name

    @property
    def current_cash(self):
        """
        :return: shop current cash mount via calculating all transactions
        """
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
        total_income = cash_in_total + cash_sale_total + int(self.capital)
        total_expanse = cash_out_total + expanse_total + cash_purchase_total
        return total_income - total_expanse

    @property
    def today_sold(self):
        """
        :return: total sold amount in today
        """
        date = datetime.today().date()
        amount = sum(
            self.shoppings.filter(
                people__people_type='customer',
                date__date=date
            ).values_list('grand_total', flat=True)
        )
        return amount

    @property
    def total_sale_due(self):
        """
        :return: total sale due amount
        """
        amount = sum(
            self.shoppings.filter(
                people__people_type='customer'
            ).values_list('due', flat=True)
        )
        return amount

    @property
    def today_purchased(self):
        """
        :return: total purchased amount in today
        """
        date = datetime.today().date()
        amount = sum(
            self.shoppings.filter(
                people__people_type='supplier',
                date__date=date
            ).values_list('grand_total', flat=True)
        )

        return amount

    @property
    def total_purchased_due(self):
        """
        :return: total purchased due amount
        """
        amount = sum(
            self.shoppings.filter(
                people__people_type='supplier'
            ).values_list('due', flat=True)
        )

        return amount

    @property
    def today_cashin(self):
        """
        :return: total cash in amount in today
        """
        date = datetime.today().date()
        amount = sum(
            self.cash_in_history.filter(
                date__date=date
            ).values_list('amount', flat=True)
        )

        return amount

    @property
    def today_cashout(self):
        """
        :return: total cash out amount in today
        """
        date = datetime.today().date()
        amount = sum(
            self.cash_out_history.filter(
                date__date=date
            ).values_list('amount', flat=True)
        )

        return amount

    @property
    def today_expanse(self):
        """
        :return: total cash out amount in today
        """
        date = datetime.today().date()
        amount = sum(
            self.expanse_history.filter(
                date__date=date
            ).values_list('amount', flat=True)
        )

        return amount
