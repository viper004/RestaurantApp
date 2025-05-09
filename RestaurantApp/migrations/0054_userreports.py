# Generated by Django 5.1.4 on 2025-04-06 05:35

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('RestaurantApp', '0053_restaurants_approval_status'),
    ]

    operations = [
        migrations.CreateModel(
            name='UserReports',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('text', models.CharField(max_length=500)),
                ('restuarant_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='RestaurantApp.restaurants')),
                ('user_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='RestaurantApp.users')),
            ],
        ),
    ]
