# Generated by Django 5.1.4 on 2025-02-09 08:16

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('RestaurantApp', '0015_alter_staffs_restaurant_name'),
    ]

    operations = [
        migrations.AlterField(
            model_name='staffs',
            name='restaurant_name',
            field=models.ForeignKey(default=True, on_delete=django.db.models.deletion.CASCADE, to='RestaurantApp.restaurants'),
        ),
    ]
