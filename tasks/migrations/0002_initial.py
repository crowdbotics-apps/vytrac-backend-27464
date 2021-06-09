# Generated by Django 3.2.4 on 2021-06-09 10:38

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('calendars', '0002_initial'),
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
            name='dates',
            field=models.ManyToManyField(blank=True, related_name='responsible', to='calendars.Event'),
        ),
        migrations.AddField(
            model_name='tasks',
            name='pations',
            field=models.ManyToManyField(blank=True, related_name='pations_daily_plan', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='tasks',
            name='responsible',
            field=models.ManyToManyField(blank=True, related_name='responsible', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='tasks',
            name='user',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='tasks_assigned', to=settings.AUTH_USER_MODEL, verbose_name='assigned to'),
        ),
    ]
