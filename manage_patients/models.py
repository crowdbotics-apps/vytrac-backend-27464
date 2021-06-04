# noinspection PyPackageRequirements
from address.models import AddressField
from django.conf import settings
from django.db import models
from safedelete.models import SafeDeleteModel

from users.models import PHONE_NUMBER_REGEX, User


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
    cost = models.PositiveIntegerField(blank=True, null=True)
    serveces = models.CharField(choices=rosters, max_length=50, blank=True)


class EmergencyContact(models.Model):
    first_name = models.CharField(max_length=50, blank=True)
    last_name = models.CharField(max_length=50, blank=True)
    last_name = models.CharField(max_length=50, blank=True)
    phone_number = models.TextField(
        max_length=500, blank=True, null=True, validators=[PHONE_NUMBER_REGEX])
    second_phone_number = models.TextField(
        max_length=500, blank=True, null=True, validators=[PHONE_NUMBER_REGEX])

    RCHOICES = (
        ('family', 'family'),
        ('friend', 'friend'),
        ('cousin', 'cousin'),
        ('siblings', 'siblings'),
        ('parent', 'parent'),
        ('partner', 'partner'),

    )
    is_done = models.BooleanField(default=False)
    relationship = models.CharField(
        max_length=50, choices=RCHOICES, blank=True)


class Insurance(SafeDeleteModel):
    primary = models.CharField(max_length=50, blank=True)
    secondary = models.CharField(max_length=50, blank=True)
    subscriber = models.CharField(max_length=50, blank=True)
    number = models.PositiveBigIntegerField(max_length=50, blank=True)
    group_number = models.PositiveBigIntegerField(max_length=50, blank=True)


class PrimaryCarePhysician(SafeDeleteModel):
    full_name = models.CharField(max_length=50, blank=True)
    phone_number = models.TextField(
        max_length=500, blank=True, null=True, validators=[PHONE_NUMBER_REGEX])
    address = AddressField(related_name='PCP+', blank=True, null=True)
    office_phone = models.TextField(
        max_length=500, blank=True, null=True, validators=[PHONE_NUMBER_REGEX])
    office_fax = models.CharField(max_length=50, blank=True)


class Language(models.Model):
    name = models.CharField(max_length=50, blank=True)


class Ethnicity(models.Model):
    name = models.CharField(max_length=50, blank=True)


class Race(models.Model):
    name = models.CharField(max_length=50, blank=True)


class Religion(models.Model):
    name = models.CharField(max_length=50, blank=True)


class Profile(SafeDeleteModel):
    # https://www.django-rest-framework.org/api-guide/relations/#generic-relationships
    # TODO return the assined dates/apoentments by ralations serializer
    # TODO I should be able to see the task detail of patients.

    native_langauge = models.OneToOneField(
        Language,
        null=True,
        blank=True,
        on_delete=models.CASCADE,
        primary_key=False,
    )

    other_langauge = models.ManyToManyField(
        Language, related_name='Profileother_langauge', blank=True)
    gender_identity = models.CharField(max_length=50, blank=True)
    marital_status = models.CharField(max_length=50, blank=True)
    race = models.OneToOneField(
        Race,
        null=True,
        blank=True,
        on_delete=models.CASCADE,
        primary_key=False,
    )
    ethnicity = models.OneToOneField(
        Ethnicity,
        null=True,
        blank=True,
        on_delete=models.CASCADE,
        primary_key=False,
    )
    religion = models.OneToOneField(
        Religion,
        null=True,
        blank=True,
        on_delete=models.CASCADE,
        primary_key=False,
    )

    insurance = models.OneToOneField(
        Insurance,
        null=True,
        blank=True,
        on_delete=models.CASCADE,
        primary_key=False,
    )
    primary_care_physician = models.OneToOneField(
        PrimaryCarePhysician,
        null=True,
        blank=True,
        on_delete=models.CASCADE,
        primary_key=False,
    )
    emergency_contact = models.ManyToManyField(
        EmergencyContact, related_name='Profile_emergency_contact', blank=True)
    # plan = #TODO

    date_created = models.DateTimeField(auto_now_add=True, null=True)
    created_by = models.ForeignKey(
        User, related_name='Patient_Profile_created_by', on_delete=models.DO_NOTHING, null=True,)
    # Note: Assigned_to = care_taker
    care_taker = models.ManyToManyField(
        User, help_text='providers, doktors, neuroses..', related_name='Patient_Profile_created_care_taker', blank=True)
    is_active = models.BooleanField(default=False)
    is_adhering = models.BooleanField(default=False)

    # Display patient Engagement(booked_servces, ... ) on dashboard toggle
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

            ('view_Profile.prescriptions_field', "Can view prescriptions"),
            ('view_Profile.symptoms_field', "Can view symptoms"),
            ('change_Profile.prescriptions_field', "Can change prescriptions"),
            ('change_Profile.symptoms_field', "Can change symptoms"),
        )

# TODO make view for this


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
    priority = models.CharField(
        max_length=50, choices=RCHOICES, blank=True)
    pations = models.ManyToManyField(
        User, related_name='pations_number', blank=True)


# TODO make view for this
class Goals(models.Model):
    name = models.CharField(max_length=200, null=True, unique=True)
    RCHOICES = (
        ('low', 'low'),
        ('averge', 'averge'),
        ('heigh', 'heigh'),)
    priority = models.CharField(
        max_length=50, choices=RCHOICES, blank=True)
    reason = models.CharField(max_length=200, blank=True)
    informations = models.CharField(max_length=200, blank=True)


class Thresholds(models.Model):
    name = models.CharField(max_length=200, null=True, unique=True)
    RCHOICES = (
        ('low', 'low'),
        ('averge', 'averge'),
        ('heigh', 'heigh'),)
    priority = models.CharField(
        max_length=50, choices=RCHOICES, blank=True)
    reason = models.CharField(max_length=200, blank=True)
    informations = models.CharField(max_length=200, blank=True)


class Reports(SafeDeleteModel):
    title = models.CharField(max_length=30, unique=True)

    RCHOICES = (
        ('low', 'low'),
        ('averge', 'averge'),
        ('heigh', 'heigh'),)
    priority = models.CharField(
        max_length=50, choices=RCHOICES, blank=True)
    related_to = models.ForeignKey(
        settings.AUTH_USER_MODEL, related_name='Reports_related_name', null=True, on_delete=models.SET_NULL)


class CPTcode(SafeDeleteModel):
    code = models.CharField(max_length=30, unique=True)


class Payment(SafeDeleteModel):
    qualified_CPTs = models.ManyToManyField(
        CPTcode, related_name='who_can_see_comment', blank=True)
    # or
    # qualified_CPTs = models.OneToOneField(
    #         CPTcode,
    #         null=True,
    #         blank=True,
    #         on_delete=models.CASCADE,
    #         primary_key=False,
    #     )
    eligible = models.BooleanField(default=False)
    report_generated = models.BooleanField(default=False)
    date_created = models.DateTimeField(auto_now_add=True, null=True)
    is_payed = models.BooleanField(default=False)
    amount = models.CharField(max_length=50, blank=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='Payment_user',
                             on_delete=models.DO_NOTHING, null=True,)
