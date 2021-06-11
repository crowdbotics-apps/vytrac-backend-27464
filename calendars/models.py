from django.conf import settings
from django.db import models
from safedelete.models import SafeDeleteModel

from Functions.MyViews import Rec
from users.models import User


class DateType(SafeDeleteModel):
    name = models.CharField(max_length=30, unique=False)
    description = models.CharField(
        max_length=30, unique=False, null=True, blank=True)


REC = (
    ('0 G day', 'Every day.'),

)


class Event(SafeDeleteModel):
    title = models.CharField(max_length=30, null=True, blank=True)
    date_type = models.ForeignKey(
        DateType, related_name='Model', on_delete=models.DO_NOTHING, null=True,)
    description = models.TextField(max_length=9999, blank=True, null=True)
    start = models.DateField(null=True, blank=True)
    end = models.DateField(null=True, blank=True)
    from_time = models.TimeField(null=True, blank=True, )
    to_time = models.TimeField(null=True, blank=True)
    date_created = models.DateTimeField(auto_now_add=True, null=True)
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    users = models.ManyToManyField(
        settings.AUTH_USER_MODEL, related_name='events',  blank=True)
    recurrence = Rec(choices=REC, blank=True, null=True)
    seen_by = models.ManyToManyField(
        settings.AUTH_USER_MODEL, related_name='seen_by', blank=True)

    is_archived = models.BooleanField(default=False)
    # TODO Automate appoentment imporatnace
    # if a patient with vital = priority meduam
    # if a atient with 2 vitals = priority heigh
    RCHOICES = (
        ('low', 'low'),
        ('averge', 'averge'),
        ('heigh', 'heigh'),)
    priority = models.CharField(
        max_length=50, choices=RCHOICES, blank=True)

    class Meta:
        get_latest_by = 'date_created'

    # def save(self,*args, **kwargs):
    # TODO add the apientment validations logic here.
    # 🔴this could be not a good idea because you can't have the loged in user
    # print(self.start >= datetime.datetime.now())
    # print(self.end)
    # print('======================')
    # print(settings.AUTH_USER_MODEL)
    # print('======================')
    # if xxx:
    #     raise ValidationError(
    #         _("You should choose one, either every day or every month or every year"),)
    # super().save(args, keyarg)
