# Generated by Django 3.0.8 on 2021-06-22 03:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0024_certification_certificatepdf'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='usertype',
            field=models.CharField(default='Student', max_length=15),
        ),
    ]
