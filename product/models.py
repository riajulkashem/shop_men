from django.core.exceptions import ObjectDoesNotExist
from django.db import models

from utilities.abstract_model import StatusModel


class Brand(StatusModel):
    shop = models.ForeignKey('pos.Shop', on_delete=models.PROTECT,
                             related_name='brands')
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField()

    def __str__(self):
        return self.name


class Category(StatusModel):
    shop = models.ForeignKey('pos.Shop', on_delete=models.PROTECT,
                             related_name='categories')
    name = models.CharField(max_length=100, unique=True)
    unit = models.CharField(max_length=50)
    description = models.TextField()

    def __str__(self):
        return self.name

    class Meta:
        unique_together = ['shop', 'name']


class Product(StatusModel):
    shop = models.ForeignKey('pos.Shop', on_delete=models.PROTECT,
                             related_name='products')
    name = models.CharField(max_length=100)
    description = models.TextField()
    brand = models.ForeignKey(Brand, on_delete=models.PROTECT,
                              related_name='products')
    category = models.ForeignKey(Category, on_delete=models.PROTECT,
                                 related_name='products')
    photo = models.ImageField(
        upload_to='product/photo/', null=True, blank=True)
    purchase_price = models.FloatField()
    sell_price = models.FloatField()
    stock = models.IntegerField()
    alert_quantity = models.IntegerField(null=True, blank=True)

    def __str__(self):
        return self.name

    def delete(self, *args, **kargs):
        self.photo.delete()
        super().delete(*args, **kargs)

    def save(self, *args, **kwargs):
        try:
            this = Product.objects.get(id=self.id)
            if this.photo != self.photo:
                this.photo.delete(save=False)
        except ObjectDoesNotExist:
            pass
        super(Product, self).save(*args, **kwargs)
