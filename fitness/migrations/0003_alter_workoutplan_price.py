# Generated by Django 3.2 on 2025-04-30 10:50

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('fitness', '0002_auto_20250430_0951'),
    ]

    operations = [
        migrations.AlterField(
            model_name='workoutplan',
            name='price',
            field=models.DecimalField(decimal_places=2, default=0.5, max_digits=10, validators=[django.core.validators.MinValueValidator(0.5)]),
        ),
    ]
