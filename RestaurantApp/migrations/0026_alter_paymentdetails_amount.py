# Generated by Django 5.1.4 on 2025-02-26 06:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('RestaurantApp', '0025_paymentdetails'),
    ]

    operations = [
        migrations.AlterField(
            model_name='paymentdetails',
            name='amount',
            field=models.IntegerField(default=0),
        ),
    ]
