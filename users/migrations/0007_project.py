# Generated by Django 3.0.8 on 2021-06-06 13:42

import datetime
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('users', '0006_auto_20210606_0856'),
    ]

    operations = [
        migrations.CreateModel(
            name='Project',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255, null=True)),
                ('status', models.BooleanField(default=False)),
                ('startDate', models.DateField(default=datetime.date(2021, 6, 6))),
                ('completionDate', models.DateField(blank=True, null=True)),
                ('associated', models.CharField(max_length=255, null=True)),
                ('projectURL', models.URLField(blank=True)),
                ('description', models.TextField(blank=True, max_length=1024, null=True)),
                ('owner', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
