# Generated by Django 5.1.4 on 2025-03-03 10:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('RestaurantApp', '0030_alter_usercart_cartid'),
    ]

    operations = [
        migrations.AlterField(
            model_name='paymentdetails',
            name='cart_id',
            field=models.CharField(max_length=100),
        ),
    ]
