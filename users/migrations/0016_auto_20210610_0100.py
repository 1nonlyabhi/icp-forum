# Generated by Django 3.0.8 on 2021-06-09 19:30

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0015_profile_rollno'),
    ]

    operations = [
        migrations.AlterField(
            model_name='certification',
            name='issueDate',
            field=models.DateField(default=datetime.date(2021, 6, 10)),
        ),
        migrations.AlterField(
            model_name='profile',
            name='image',
            field=models.ImageField(default='default.png', upload_to='uploads/profile_pics'),
        ),
        migrations.AlterField(
            model_name='project',
            name='startDate',
            field=models.DateField(default=datetime.date(2021, 6, 10)),
        ),
    ]