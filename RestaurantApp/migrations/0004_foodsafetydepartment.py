# Generated by Django 5.1.4 on 2025-02-02 09:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('RestaurantApp', '0003_staffs'),
    ]

    operations = [
        migrations.CreateModel(
            name='FoodSafetyDepartment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('department_id', models.IntegerField(max_length=5)),
                ('contact', models.CharField(max_length=15)),
            ],
        ),
    ]
