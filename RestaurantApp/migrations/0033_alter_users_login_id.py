# Generated by Django 5.1.4 on 2025-03-07 06:32

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('RestaurantApp', '0032_usercart_payment_status'),
    ]

    operations = [
        migrations.AlterField(
            model_name='users',
            name='login_id',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='RestaurantApp.login'),
        ),
    ]
