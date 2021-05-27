# Generated by Django 3.2.3 on 2021-05-24 15:03

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='CPTcode',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('deleted', models.DateTimeField(editable=False, null=True)),
                ('code', models.CharField(max_length=30, unique=True)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Payment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('deleted', models.DateTimeField(editable=False, null=True)),
                ('eligible', models.BooleanField(default=False)),
                ('report_generated', models.BooleanField(default=False)),
                ('date_created', models.DateTimeField(auto_now_add=True, null=True)),
                ('is_payed', models.BooleanField(default=False)),
                ('amount', models.CharField(blank=True, max_length=50)),
                ('qualified_CPTs', models.ManyToManyField(blank=True, related_name='who_can_see_comment', to='billings.CPTcode')),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
