# Generated by Django 3.0.8 on 2021-06-06 03:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0004_auto_20210606_0834'),
    ]

    operations = [
        migrations.AlterField(
            model_name='certification',
            name='expirationDate',
            field=models.DateField(blank=True),
        ),
    ]
