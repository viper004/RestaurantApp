# Generated by Django 5.1.4 on 2025-04-29 08:15

import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('RestaurantApp', '0062_announcements'),
    ]

    operations = [
        migrations.AddField(
            model_name='announcements',
            name='subject',
            field=models.CharField(default=django.utils.timezone.now, max_length=200),
            preserve_default=False,
        ),
    ]
