# Generated by Django 5.1.4 on 2025-02-23 09:16

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('RestaurantApp', '0022_alter_usercart_resturant_id'),
    ]

    operations = [
        migrations.RenameField(
            model_name='usercart',
            old_name='resturant_id',
            new_name='resturant_loginid',
        ),
    ]
