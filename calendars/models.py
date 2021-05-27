from django.db import models
from safedelete.models import SafeDeleteModel, NO_DELETE
from users.models import User
from django.conf import settings


class DateType(SafeDeleteModel):
    name = models.CharField(max_length=30, unique=False)
    description = models.CharField(
        max_length=30, unique=False, null=True, blank=True)


class Date(SafeDeleteModel):
    title = models.CharField(max_length=30, null=True, blank=True)
    date_type = models.ForeignKey(
        DateType, related_name='Model', on_delete=models.DO_NOTHING, null=True,)
    description = models.TextField(max_length=9999, blank=True, null=True)
    start = models.DateTimeField(null=True)
    end = models.DateTimeField(null=True)
    date_created = models.DateTimeField(auto_now_add=True, null=True)
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    users = models.ManyToManyField(User, related_name='date_with', blank=True)
