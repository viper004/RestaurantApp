# Generated by Django 5.1.4 on 2025-05-07 06:24

import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('RestaurantApp', '0077_alter_login_email'),
    ]

    operations = [
        migrations.AddField(
            model_name='restaurants',
            name='about',
            field=models.TextField(default=django.utils.timezone.now),
            preserve_default=False,
        ),
    ]
