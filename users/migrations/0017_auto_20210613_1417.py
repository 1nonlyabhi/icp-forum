# Generated by Django 3.0.8 on 2021-06-13 08:47

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0016_auto_20210610_0100'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='usertype',
            field=models.CharField(default='Student', max_length=15),
        ),
        migrations.AlterField(
            model_name='certification',
            name='issueDate',
            field=models.DateField(default=datetime.date(2021, 6, 13)),
        ),
        migrations.AlterField(
            model_name='project',
            name='startDate',
            field=models.DateField(default=datetime.date(2021, 6, 13)),
        ),
    ]
