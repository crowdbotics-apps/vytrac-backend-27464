# Generated by Django 3.2.3 on 2021-05-27 15:16

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('calendars', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AddField(
            model_name='date',
            name='created_by',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='date',
            name='date_type',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='Model', to='calendars.datetype'),
        ),
        migrations.AddField(
            model_name='date',
            name='users',
            field=models.ManyToManyField(blank=True, related_name='date_with', to=settings.AUTH_USER_MODEL),
        ),
    ]
