from django.conf import settings
from django.contrib.auth.models import Group
from django.db import models
from safedelete.models import SafeDeleteModel, NO_DELETE
from users.models import User


class Symptoms(SafeDeleteModel):
    title = models.CharField(max_length=30, unique=True)
    description = models.TextField(max_length=400)


rosters = (
    ('(99201–99215)', 'Office/other outpatient services'),
    ('(99217–99220)', 'Hospital observation services'),
    ('(99221–99239)', 'Hospital inpatient services'),
    ('(99241–99255)', 'Consultations'),
    ('(99281–99288)', 'Emergency department services'),
    ('(99291–99292)', 'Critical care services'),
    ('(99304–99318)', 'Nursing facility services'),
    ('(99324–99337)', 'Domiciliary, rest home (boarding home) or custodial care services'),
    ('(99339–99340)', 'Domiciliary, rest home (assisted living facility), or home care plan oversight services'),
    ('(99341–99350)', 'Home health services'),
    ('(99354–99360)', 'Prolonged services'),
    ('(99363–99368)', 'Case management services'),
    ('(99374–99380)', 'Care plan oversight services'),
    ('(99381–99429)', 'Preventive medicine services'),
    ('(99441–99444)', 'Non-face-to-face physician services'),
    ('(99450–99456)', 'Special evaluation and management services'),
    ('(99460–99465)', 'Newborn care services'),
    ('(99466–99480)', 'Inpatient neonatal intensive, and pediatric/neonatal critical, care services'),
    ('(99487–99489)', 'Complex chronic care coordination services'),
    ('(99495–99496)', 'Transitional care management services'),
    ('(99499)', 'Other evaluation and management services'),

)


class Roster(SafeDeleteModel):
    title = models.CharField(max_length=30, unique=True)
    # TODO CPT list
    # serveces = models.CharField(choices=rosters, max_length=50, blank=True)


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
    blood_pressure = models.CharField(max_length=100, blank=True, null=True)
    age = models.PositiveIntegerField(blank=True, null=True)

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
