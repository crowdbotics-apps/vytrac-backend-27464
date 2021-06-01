
from Myclasses import Rec
from multiselectfield import MultiSelectField
from django.db.models.fields.related import ManyToManyField
from safedelete.models import (
    SafeDeleteModel,
    NO_DELETE
)
from django.core.validators import MaxLengthValidator, RegexValidator
from django.core.exceptions import ValidationError
from rest_framework.authtoken.models import Token
from django.dispatch import receiver
from django.db.models.signals import post_save
from django.db import models

# Create your models here.
from django.db import models
from django.utils import deconstruct, timezone
from django.contrib.auth.models import User, Group, AbstractUser, AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.conf import settings
from django.contrib.auth import get_user_model
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.models import Group
StyleTitleFormat = RegexValidator(r'^[^\s]+$', 'spaces not allowed')


# @receiver(post_save, sender=settings.AUTH_USER_MODEL)
# def create_auth_token(sender, instance=None, created=False, **kwargs):
#     if created:
#         Token.objects.create(user=instance)


PHONE_NUMBER_REGEX = RegexValidator(
    r'^[+]*[(]{0,1}[0-9]{1,4}[)]{0,1}[-\s\./0-9]*$', 'invalid phone number')

USERNAME = RegexValidator(
    r'^[a-zA-Z ]+$', 'only letter from a-z are allowed')


REC = (
    ('0 G day', 'Every day.'),

)


class Availablity(SafeDeleteModel):
    title = models.CharField(max_length=30, null=True, blank=True)
    description = models.TextField(max_length=9999, blank=True, null=True)
    start = models.DateTimeField(null=True)
    end = models.DateTimeField(null=True)
    date_created = models.DateTimeField(auto_now_add=True, null=True)
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    recurrence = Rec(blank=True, choices=REC)


models_names = (('patien profiel', 'patien profiel'),)


class Settings(SafeDeleteModel):
    # notifcaions settings/report settings
    #
    watch = models.CharField(max_length=50, choices=models_names, blank=True)
    settings_type = models.CharField(max_length=30, choices=(
        ('notifcations', 'notifcations settings'), ('reporet', 'reporet tashbord settings')), unique=True)
    see_all = models.BooleanField(default=False)


class User(AbstractUser, PermissionsMixin):
    username = models.CharField(
        max_length=30, unique=True, validators=[USERNAME])
    email = models.EmailField(max_length=250, unique=True)
    first_name = models.CharField(max_length=30, blank=True, null=True)
    last_name = models.CharField(max_length=30, blank=True, null=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    is_email_verified = models.BooleanField(default=False)
    is_role_verified = models.BooleanField(default=False)
    date_joined = models.DateTimeField(default=timezone.now)
    receive_newsletter = models.BooleanField(default=False)
    birth_date = models.DateTimeField(blank=True, null=True)
    address = models.CharField(max_length=300,  blank=True, null=True)
    city = models.CharField(max_length=30, blank=True, null=True)
    about_me = models.TextField(max_length=500, blank=True, null=True)
    phone_number = models.TextField(
        max_length=500, blank=True, null=True, validators=[PHONE_NUMBER_REGEX])
    imageUrl = models.CharField(max_length=900, blank=True, null=True)
    # TODO if not avablae then you can't create apoentment
    date_avalable = models.ManyToManyField(
        Availablity, related_name='date_avalable', blank=True)
    settings = models.ManyToManyField(
        Settings, related_name='who_can_see_comment', blank=True)
    age = models.CharField(max_length=50, blank=True)
    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email', ]

    class Meta:
        permissions = (
            ('view_user.phone_number_field', "Can view phone number"),
            ('change_user.phone_number_field', "Can change phone number"),
        )
