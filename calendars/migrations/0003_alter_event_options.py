# Generated by Django 3.2.4 on 2021-06-09 12:08

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('calendars', '0002_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='event',
            options={'get_latest_by': 'date_created'},
        ),
    ]
