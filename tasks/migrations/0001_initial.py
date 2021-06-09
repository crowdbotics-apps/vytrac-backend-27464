# Generated by Django 3.2.4 on 2021-06-09 10:38

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Tasks',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=200, verbose_name='title')),
                ('description', models.TextField(blank=True, max_length=2000, null=True, verbose_name='description')),
                ('resolution', models.TextField(blank=True, max_length=2000, null=True, verbose_name='resolution')),
                ('deadline', models.DateTimeField(blank=True, null=True, verbose_name='deadline')),
                ('state', models.CharField(choices=[('to-do', 'To Do'), ('in_progress', 'In Progress'), ('blocked', 'Blocked'), ('done', 'Done'), ('dismissed', 'Dismissed')], default='to-do', max_length=20, verbose_name='state')),
                ('priority', models.CharField(choices=[('00_low', 'Low'), ('10_normal', 'Normal'), ('20_high', 'High'), ('30_critical', 'Critical'), ('40_blocker', 'Blocker')], default='10_normal', max_length=20, verbose_name='priority')),
                ('date_created', models.DateTimeField(auto_now_add=True, verbose_name='created at')),
                ('last_modified', models.DateTimeField(auto_now=True, verbose_name='last modified')),
                ('type', models.CharField(choices=[('daily_plan', 'Daily plan'), ('task', 'task'), ('emergency', 'Emergency')], default='10_normal', max_length=20, verbose_name='type')),
            ],
            options={
                'verbose_name': 'Tasks',
                'verbose_name_plural': 'Taskss',
            },
        ),
    ]
