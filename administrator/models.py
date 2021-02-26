from django.db import models

from pos.models import Shop
from utilities.abstract_model import StatusModel


class NotifyUser(StatusModel):
    msg = models.TextField()
    shop = models.ManyToManyField(Shop, related_name='msg_list')

    def __str__(self):
        return self.msg
