# Generated by Django 3.0.8 on 2021-06-08 19:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0013_auto_20210609_0120'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='extraskills',
            field=models.CharField(blank=True, max_length=255),
        ),
        migrations.AlterField(
            model_name='profile',
            name='techskills',
            field=models.CharField(blank=True, max_length=255),
        ),
    ]
