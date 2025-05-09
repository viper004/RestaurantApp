# Generated by Django 5.1.4 on 2025-02-08 07:27

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('RestaurantApp', '0004_foodsafetydepartment'),
    ]

    operations = [
        migrations.AddField(
            model_name='foodsafetydepartment',
            name='login_id',
            field=models.ForeignKey(default=0, on_delete=django.db.models.deletion.CASCADE, to='RestaurantApp.login'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='restaurants',
            name='login_id',
            field=models.ForeignKey(default=0, on_delete=django.db.models.deletion.CASCADE, to='RestaurantApp.login'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='staffs',
            name='login_id',
            field=models.ForeignKey(default=0, on_delete=django.db.models.deletion.CASCADE, to='RestaurantApp.login'),
            preserve_default=False,
        ),
    ]
