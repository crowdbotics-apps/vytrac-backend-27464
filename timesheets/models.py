
from safedelete.models import SafeDeleteModel, NO_DELETE
from django.db.models import signals
from django.dispatch import receiver
from django.db import models
from django.conf import settings
from patientsprofiles.models import PatientProfile
from users.models import User


class ChangeTrack(SafeDeleteModel):
    changed_by = models.ForeignKey(
        settings.AUTH_USER_MODEL, related_name='user', on_delete=models.DO_NOTHING, null=True,)
    date = models.DateTimeField(auto_now_add=True, null=True)


class PatientProfileTracker(ChangeTrack):
    user = models.OneToOneField(
        User,
        null=True,
        blank=True,
        on_delete=models.CASCADE,
        primary_key=False,
    )
    prescriptions = models.TextField(max_length=999, blank=True, null=True)
    symptoms = models.ManyToManyField(
        PatientProfile, related_name='symptoms_tracker', blank=True)


class DalyPlanTracker(ChangeTrack):
    '''
    Adherence/activity (chart)
    Last interaction with Daily Plan
    '''
    title = models.CharField(max_length=30, unique=True)


# class ModelNameList(ListView):
    # Avg time Spent responding to Alerts for each person
    # filter by group name
    # filter by permissions

@receiver(signals.post_save)
def __init__(instance, sender, signal, *args, **kwargs):
    # TODO A3
    # if notifcations seen
    # 1.  registaer notifcation is seend, seen date, seen by who
    # 2. Last interaction with Daily Plan
    # 3.  notifcation created date - notifcation seend date
    pass
