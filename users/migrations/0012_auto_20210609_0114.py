# Generated by Django 3.0.8 on 2021-06-08 19:44

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0011_auto_20210608_2327'),
    ]

    operations = [
        migrations.AlterField(
            model_name='certification',
            name='issueDate',
            field=models.DateField(default=datetime.date(2021, 6, 9)),
        ),
        migrations.AlterField(
            model_name='profile',
            name='birth_date',
            field=models.DateField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='project',
            name='startDate',
            field=models.DateField(default=datetime.date(2021, 6, 9)),
        ),
    ]
