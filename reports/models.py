from django.conf import settings
from django.db import models
from safedelete.models import SafeDeleteModel, NO_DELETE

# Create your models here.


class Report(SafeDeleteModel):
    title = models.CharField(max_length=30, unique=True)

    RCHOICES = (
        ('low', 'low'),
        ('averge', 'averge'),
        ('heigh', 'heigh'),)
    importance = models.CharField(
        max_length=50, choices=RCHOICES, blank=True)
    related_to = models.ForeignKey(
        settings.AUTH_USER_MODEL, related_name='Reports_related_name', null=True, on_delete=models.SET_NULL)
