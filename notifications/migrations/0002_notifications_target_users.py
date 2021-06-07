# Generated by Django 3.2.4 on 2021-06-07 09:19

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('notifications', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AddField(
            model_name='notifications',
            name='target_users',
            field=models.ManyToManyField(blank=True, null=True, related_name='Notification_target_user', to=settings.AUTH_USER_MODEL),
        ),
    ]
