import inspect
from django.db import models
from safedelete.models import SafeDeleteModel, NO_DELETE
from users.models import User
from django.conf import settings
from multiselectfield import MultiSelectField
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
from django import forms

REC = (
    ('0 G day', 'Every day.'),
    ('0 month', 'Every month.'),
    ('0 year', 'Every year.'),
    ('1 sunday', 'Every sunday.'),
    ('1 monday', 'Every monday.'),
    ('1 tuesday', 'Every tuesday.'),
    ('1 wednesday', 'Every wednesday.'),
    ('1 thursday', 'Every thursday.'),
    ('1 friday', 'Every friday.'),
    ('1 saturday', 'Every saturday.'),

    #  TODO recurnce on spesifc months
    # ('2 aprile', 'Every aprile.'),
    # ('2 june', 'Every june.'),
    # ('2 julay', 'Every julay.'),
    # ('2 aprile', 'Every aprile.'),
    # ('2 aprile', 'Every aprile.'),
    # ('2 aprile', 'Every aprile.'),
    # ('2 aprile', 'Every aprile.'),
    # ('2 julay', 'Every julay.'),
    # ('2 aprile', 'Every aprile.'),
    # ('2 aprile', 'Every aprile.'),
    # ('2 aprile', 'Every aprile.'),
    # ('2 aprile', 'Every aprile.'),

)


class DateType(SafeDeleteModel):
    name = models.CharField(max_length=30, unique=False)
    description = models.CharField(
        max_length=30, unique=False, null=True, blank=True)


def myfunction(self, *args, **keyarg):
    if str(self).count('0') > 1:
        raise ValidationError(
            _("You should choose one, either every day or every month or every year"),)

    if str(self).count('G') >= 1 and str(self).count('1') >= 1:
        days = list(filter(lambda k: '1' in k, self))
        fD = []
        for day in days:
            fD.append(day.replace('1 ', '').title())
        raise ValidationError(
            _("If it reapeate every day it will repeated on "+str(fD)+" as well"),)


class Rec(MultiSelectField):
    def _choices_is_value(self, *args, **keyarg):
        print('_choices_is_value======================')
        self.validators = [myfunction]
        return super()._choices_is_value(*args, **keyarg)


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
    recurrence = Rec(choices=REC, blank=True)
