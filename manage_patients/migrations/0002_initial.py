# Generated by Django 3.2.4 on 2021-06-02 13:24

import address.models
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('manage_patients', '0001_initial'),
        ('address', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='reports',
            name='related_to',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='Reports_related_name', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='profile',
            name='booked_servces',
            field=models.ManyToManyField(blank=True, related_name='booked_servces', to='manage_patients.Roster'),
        ),
        migrations.AddField(
            model_name='profile',
            name='care_taker',
            field=models.ManyToManyField(blank=True, related_name='Patient_Profile_created_care_taker', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='profile',
            name='created_by',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='Patient_Profile_created_by', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='profile',
            name='emergency_contact',
            field=models.ManyToManyField(blank=True, related_name='Profile_emergency_contact', to='manage_patients.EmergencyContact'),
        ),
        migrations.AddField(
            model_name='profile',
            name='ethnicity',
            field=models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='manage_patients.ethnicity'),
        ),
        migrations.AddField(
            model_name='profile',
            name='insurance',
            field=models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='manage_patients.insurance'),
        ),
        migrations.AddField(
            model_name='profile',
            name='native_langauge',
            field=models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='manage_patients.language'),
        ),
        migrations.AddField(
            model_name='profile',
            name='other_langauge',
            field=models.ManyToManyField(blank=True, related_name='Profileother_langauge', to='manage_patients.Language'),
        ),
        migrations.AddField(
            model_name='profile',
            name='primary_care_physician',
            field=models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='manage_patients.primarycarephysician'),
        ),
        migrations.AddField(
            model_name='profile',
            name='race',
            field=models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='manage_patients.race'),
        ),
        migrations.AddField(
            model_name='profile',
            name='religion',
            field=models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='manage_patients.religion'),
        ),
        migrations.AddField(
            model_name='profile',
            name='symptoms',
            field=models.ManyToManyField(blank=True, related_name='symptoms', to='manage_patients.Symptoms'),
        ),
        migrations.AddField(
            model_name='profile',
            name='user',
            field=models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='primarycarephysician',
            name='address',
            field=address.models.AddressField(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='PCP+', to='address.address'),
        ),
        migrations.AddField(
            model_name='payment',
            name='qualified_CPTs',
            field=models.ManyToManyField(blank=True, related_name='who_can_see_comment', to='manage_patients.CPTcode'),
        ),
        migrations.AddField(
            model_name='payment',
            name='user',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='Payment_user', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='dalyplan',
            name='created_by',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='Model', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='dalyplan',
            name='pations',
            field=models.ManyToManyField(blank=True, related_name='pations_number', to=settings.AUTH_USER_MODEL),
        ),
    ]
