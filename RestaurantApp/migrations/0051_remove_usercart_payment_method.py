# Generated by Django 5.1.4 on 2025-04-02 17:37

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('RestaurantApp', '0050_paymentdetails_pickup'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='usercart',
            name='payment_method',
        ),
    ]
