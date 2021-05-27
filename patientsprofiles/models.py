from django.conf import settings
from django.contrib.auth.models import Group
from django.db import models
from safedelete.models import SafeDeleteModel, NO_DELETE
from users.models import User


class Symptoms(SafeDeleteModel):
    title = models.CharField(max_length=30, unique=True)
    description = models.TextField(max_length=400)


class Roster(SafeDeleteModel):
    title = models.CharField(max_length=30, unique=True)


class PatientProfile(SafeDeleteModel):
    # plan = #TODO
    date_created = models.DateTimeField(auto_now_add=True, null=True)
    created_by = models.ForeignKey(
        User, related_name='Patient_Profile_created_by', on_delete=models.DO_NOTHING, null=True,)
    # Note: Assigned_to = care_taker
    care_taker = models.ManyToManyField(
        User, related_name='Patient_Profile_created_care_taker', blank=True)
    is_active = models.BooleanField(default=False)
    is_adhering = models.BooleanField(default=False)
    booked_servces = models.ManyToManyField(
        Roster, related_name='booked_servces', blank=True)
    user = models.OneToOneField(
        User,
        null=True,
        blank=True,
        on_delete=models.CASCADE,
        primary_key=False,
    )
    prescriptions = models.TextField(max_length=999, blank=True, null=True)
    symptoms = models.ManyToManyField(
        Symptoms, related_name='symptoms', blank=True)

    class Meta:
        permissions = (
            ('view_patientprofile.prescriptions_field', "Can view prescriptions"),
            ('view_patientprofile.symptoms_field', "Can view symptoms"),
            ('change_patientprofile.prescriptions_field', "Can change prescriptions"),
            ('change_patientprofile.symptoms_field', "Can change symptoms"),
        )


class DalyPlan(SafeDeleteModel):
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL, related_name='Model', on_delete=models.DO_NOTHING, null=True,)
    date_created = models.DateTimeField(auto_now_add=True, null=True)
    RCHOICES = (
        ('low', 'low'),
        ('averge', 'averge'),
        ('heigh', 'heigh'),
    )
    is_done = models.BooleanField(default=False)
    importance = models.CharField(
        max_length=50, choices=RCHOICES, blank=True)
    pations = models.ManyToManyField(
        User, related_name='pations_number', blank=True)
