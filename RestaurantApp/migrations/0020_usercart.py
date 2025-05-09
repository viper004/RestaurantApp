# Generated by Django 5.1.4 on 2025-02-23 07:38

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('RestaurantApp', '0019_dishes_status'),
    ]

    operations = [
        migrations.CreateModel(
            name='UserCart',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('current_date', models.DateField(auto_now_add=True)),
                ('current_time', models.TimeField(auto_now_add=True)),
                ('product_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='RestaurantApp.dishes')),
                ('user_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='RestaurantApp.users')),
            ],
        ),
    ]
