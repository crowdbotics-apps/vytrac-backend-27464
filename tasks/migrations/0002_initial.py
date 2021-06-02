# Generated by Django 3.2.3 on 2021-06-02 06:20

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('tasks', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AddField(
            model_name='tasks',
            name='created_by',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='users_created', to=settings.AUTH_USER_MODEL, verbose_name='created by'),
        ),
        migrations.AddField(
            model_name='tasks',
            name='user',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='tasks_assigned', to=settings.AUTH_USER_MODEL, verbose_name='assigned to'),
        ),
    ]
