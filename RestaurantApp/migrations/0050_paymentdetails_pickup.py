# Generated by Django 5.1.4 on 2025-03-30 09:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('RestaurantApp', '0049_paymentdetails_upi_paymentdetails_upi_id'),
    ]

    operations = [
        migrations.AddField(
            model_name='paymentdetails',
            name='pickup',
            field=models.CharField(default=False, max_length=100, null=True),
        ),
    ]
