# Generated by Django 3.2.3 on 2021-05-29 12:55

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('timesheets', '0002_changetrack_by'),
    ]

    operations = [
        migrations.AddField(
            model_name='changetrack',
            name='related_to',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='related_name', to=settings.AUTH_USER_MODEL),
        ),
    ]
