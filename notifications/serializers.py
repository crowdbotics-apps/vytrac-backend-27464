from django.utils.http import urlsafe_base64_decode
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.utils.encoding import force_str
from rest_framework.exceptions import AuthenticationFailed
from drf_queryfields import QueryFieldsMixin
from rest_framework.serializers import (
    ModelSerializer,
)
from rest_framework import serializers
from . import models


class ItemsSer(serializers.ModelSerializer):
    class Meta:
        model = models.Notifications
        fields = '__all__'
