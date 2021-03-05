"""Core > models > test_user.py"""
# PYTHON IMPORTS
import logging
from sys import _getframe

from django.contrib.auth.models import (
    AbstractBaseUser, BaseUserManager, PermissionsMixin
)
from django.contrib.sessions.models import Session
from django.core.validators import RegexValidator, MinLengthValidator
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils import timezone
from django.utils.translation import gettext_lazy as _

logger = logging.getLogger(__name__)


class UserManager(BaseUserManager):
    """User Manager overridden from BaseUserManager for User"""

    def _create_user(self, phone, password=None, **extra_fields):
        """Creates and returns a new user using an email address"""
        if not phone:  # check for an empty email
            logger.error(  # prints class and function name
                f"{self.__class__.__name__}.{_getframe().f_code.co_name} "
                f"User must set an email address"
            )
            raise AttributeError("User must set an email address")
        else:
            logger.debug(  # prints class and function name
                f"{self.__class__.__name__}.{_getframe().f_code.co_name} "
                f"User Phone: {phone}"
            )

        # create user
        user = self.model(phone=phone, **extra_fields)
        user.set_password(password)  # hashes/encrypts password
        user.save(using=self._db)  # safe for multiple databases
        logger.debug(  # prints class and function name
            f"{self.__class__.__name__}.{_getframe().f_code.co_name} "
            f"User created: {user}"
        )
        return user

    def create_user(self, phone, password=None, **extra_fields):
        """Creates and returns a new user using an email address"""
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        logger.debug(  # prints class and function name
            f"{self.__class__.__name__}.{_getframe().f_code.co_name} "
            f"Creating user: phone={phone}, extra_fields={extra_fields}"
        )
        return self._create_user(phone, password, **extra_fields)

    def create_staffuser(self, phone, password=None, **extra_fields):
        """Creates and returns a new staffuser using an email address"""
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', False)
        logger.debug(  # prints class and function name
            f"{self.__class__.__name__}.{_getframe().f_code.co_name} "
            f"Creating staffuser: email={phone}, extra_fields={extra_fields}"
        )
        return self._create_user(phone, password, **extra_fields)

    def create_superuser(self, phone, password=None, **extra_fields):
        """Creates and returns a new superuser using an email address"""
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        logger.debug(  # prints class and function name
            f"{self.__class__.__name__}.{_getframe().f_code.co_name} "
            f"Creating superuser: email={phone}, extra_fields={extra_fields}"
        )
        return self._create_user(phone, password, **extra_fields)


class User(
    AbstractBaseUser,
    PermissionsMixin,
):
    """
    User model that supports using email instead of username
    """
    pin = models.CharField(max_length=50)
    phone = models.CharField(
        unique=True, null=True,
        max_length=14, validators=[
            RegexValidator(
                regex=r'^(?:\+8801|01)?(\d{9})$',
                message='Invalid Phone Number'
            ), MinLengthValidator(limit_value=11)
        ]
    )
    staff_shop = models.ForeignKey(
        'pos.Shop',
        on_delete=models.PROTECT,
        related_name='staff_list',
        null=True,
        blank=True
    )
    email = models.EmailField(
        _('Email Address'), max_length=255, unique=True, null=True, blank=True
    )
    first_name = models.CharField(
        _('First Name'), max_length=255, blank=True, null=True
    )
    last_name = models.CharField(
        _('Family Name'), max_length=255, blank=True, null=True
    )
    is_staff = models.BooleanField(
        _('Staff status'), default=False, null=True
    )
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)
    objects = UserManager()  # uses the custom manager

    USERNAME_FIELD = 'phone'  # overrides username to email field

    def get_full_name(self):
        """Returns full name of User
        Return None if no names are set"""
        logger.debug(  # prints class and function name
            f"{self.__class__.__name__}.{_getframe().f_code.co_name} "
            f"Getting {self.phone}'s full name"
        )
        full_name = None  # default

        # join first name and last name
        if self.first_name:
            full_name = ''.join(self.first_name)
            if self.last_name:
                full_name += f' {self.last_name}'
        else:
            if self.last_name:
                full_name = ''.join(self.last_name)
            else:
                full_name = self.get_username()

        logger.debug(  # prints class and function name
            f"{self.__class__.__name__}.{_getframe().f_code.co_name} "
            f"Returning user's full name: {full_name}"
        )
        return full_name  # returns None if no name is set

    def get_phone_intl_format(self, prefix='+88'):
        """Returns phone number in international format
        Default prefix: +88 (Bangladesh code)
        Returns None if user has no phone number saved"""
        phone_intl = f'{prefix}{self.phone}' if self.phone else None
        logger.debug(  # prints class and function name
            f"{self.__class__.__name__}.{_getframe().f_code.co_name} "
            f"Returning phone number in international format: {phone_intl}"
        )
        return phone_intl

    def __str__(self):
        """User model string representation"""
        return f'{self.get_full_name()} ({self.phone})'

    def remove_all_sessions(self):
        user_sessions = []
        all_sessions = Session.objects.filter(expire_date__gte=timezone.now())
        for session in all_sessions:
            if str(self.pk) == session.get_decoded().get('_auth_user_id'):
                user_sessions.append(session.pk)
        return Session.objects.filter(pk__in=user_sessions).delete()

    class Meta:
        ordering = ['id']


def media_upload_path(instance, filename):
    """Returns formatted upload to path"""
    path = f'Users/{instance.user.id}/{filename}'
    logger.debug(  # prints class and function name
        f"{_getframe().f_code.co_name} Media upload path: {path}"
    )
    return path


class Profile(
    models.Model
):
    """User Profile model"""
    user = models.OneToOneField(
        User, on_delete=models.CASCADE, primary_key=True, unique=True
    )
    photo = models.ImageField(
        _('Profile Picture'), blank=True, null=True,
        upload_to=media_upload_path
    )
    bio = models.TextField(
        _('Bio'), blank=True, null=True
    )
    website = models.URLField(
        _('Website'), blank=True, null=True
    )
    birthday = models.DateField(
        _('Date of Birth'), blank=True, null=True
    )
    gender = models.CharField(
        _('Gender'), max_length=1, blank=True, null=True,
        choices=[('M', 'Male'), ('F', 'Female')]
    )
    spouse_name = models.CharField(
        _('Name of Spouse'), max_length=255, blank=True, null=True
    )
    father_name = models.CharField(
        _('Name of Father'), max_length=255, blank=True, null=True
    )
    mother_name = models.CharField(
        _('Name of Mother'), max_length=255, blank=True, null=True
    )
    nid = models.CharField(
        _('National ID'), max_length=17, unique=True, blank=True, null=True,
        validators=[RegexValidator(
            r'^(\d{10}|\d{13}|\d{17})$',
            message='Numeric 10/13/17 digits (ex: 1234567890)'
        )]
    )
    passport = models.CharField(
        _('Passport'), max_length=9, unique=True, blank=True, null=True,
        validators=[RegexValidator(
            r'^[A-Z]{2}\d{7}$',
            message='Alphanumeric 9 characters (ex: PA3456789)'
        )]
    )
    address = models.CharField(
        _('Street Address'), max_length=255, blank=True, null=True
    )
    thana = models.CharField(
        _('Thana'), max_length=255, blank=True, null=True
    )
    district = models.CharField(
        _('District'), max_length=255, blank=True, null=True
    )
    division = models.CharField(
        _('Division'), max_length=255, blank=True, null=True
    )
    postal = models.CharField(
        _('Postal Code'), max_length=4, blank=True, null=True
    )
    is_active = models.BooleanField(
        _('Active'), default=True, null=True
    )
    created = models.DateTimeField(
        _('Created At'), auto_now_add=True, null=True
    )
    updated = models.DateTimeField(
        _('Last Updated'), auto_now=True, null=True
    )
    

    @property
    def age(self):
        """Returns user's age from given birthday, else returns 0"""
        age = 0
        if self.birthday:
            age = int((timezone.now().date() - self.birthday).days / 365.25)
        logger.debug(  # prints class and function name
            f"{self.__class__.__name__}.{_getframe().f_code.co_name} "
            f"Calculated {self.user}'s age: {age}"
        )
        return age

    def __str__(self):
        """String representation of Profile model"""
        return self.user.get_full_name()


@receiver(post_save, sender=User)
def create_or_update_profile(sender, instance, created, **kwargs):
    """Creates or updates profile, when User object changes"""
    if created and instance:
        # logger.debug(  # prints class and function name
        #     f"{_getframe().f_code.co_name} Creating {instance}'s profile"
        # )
        instance.set_password(instance.pin)
        instance.save()
        Profile.objects.get_or_create(user=instance)
