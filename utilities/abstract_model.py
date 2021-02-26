from django.core.validators import RegexValidator, MinLengthValidator
from django.db import models
from user.models import User


class TimeStampedModel(models.Model):
    """
    An abstract base class model that provides self-updating
    ``created`` and ``modified`` fields.
    """
    creator = models.ForeignKey(User, on_delete=models.PROTECT)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True
        ordering = ['updated']


class StatusModel(TimeStampedModel):
    is_active = models.BooleanField(default=True)

    class Meta:
        abstract = True
        ordering = ['updated']


class TimeStampedPhoneModel(TimeStampedModel):
    phone = models.CharField(
        unique=True, null=True,
        max_length=14, validators=[
            RegexValidator(
                regex=r'^(?:\+8801|01)?(\d{9})$',
                message='Invalid Phone Number'
            ), MinLengthValidator(limit_value=11)
        ])

    class Meta:
        abstract = True
        ordering = ['updated']


class StatusPhoneModel(StatusModel):
    phone = models.CharField(
        unique=True, null=True, max_length=14,
        validators=[
            RegexValidator(
                regex=r'^(?:\+8801|01)?(\d{9})$',
                message='Invalid Phone Number'
            ), MinLengthValidator(limit_value=11)
        ]
    )

    class Meta:
        abstract = True
        ordering = ['updated']
