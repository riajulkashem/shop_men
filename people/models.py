from django.core.exceptions import ObjectDoesNotExist
from django.db import models
from django.urls import reverse

from utilities.abstract_model import StatusPhoneModel


class People(StatusPhoneModel):
    TYPE = (
        ('customer', 'Customer'),
        ('supplier', 'Supplier'),
    )
    people_type = models.CharField(max_length=50, choices=TYPE)
    shop = models.ForeignKey(
        'pos.Shop', on_delete=models.PROTECT,
        related_name='people',
        null=True
    )
    name = models.CharField(max_length=200)
    email = models.EmailField(blank=True, null=True)
    photo = models.ImageField(
        blank=True,
        upload_to='people/photo/',
        null=True
    )
    address = models.TextField(null=True)
    opening_balance = models.IntegerField(default=0)
    due = models.IntegerField(default=0)
    return_due = models.IntegerField(default=0)
    total_paid = models.IntegerField(default=0)

    def delete(self, *args, **kargs):
        self.photo.delete()
        super().delete(*args, **kargs)

    def save(self, *args, **kwargs):
        try:
            this = People.objects.get(id=self.id)
            if this.photo != self.photo:
                this.photo.delete(save=False)
        except ObjectDoesNotExist:
            pass
        super(People, self).save(*args, **kwargs)

    def __str__(self):
        return f'{self.name} ({self.phone})'

    def get_update_url(self):
        if self.people_type == 'customer':
            return reverse('people:customer_update', kwargs={'pk': 1})
        return reverse('people:supplier_update', kwargs={'pk': 1})
