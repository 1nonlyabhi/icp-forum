# Generated by Django 3.0.8 on 2021-06-09 19:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0002_auto_20210607_1440'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='attachedimage',
            field=models.ImageField(blank=True, null=True, upload_to='uploads/post_photos'),
        ),
    ]
