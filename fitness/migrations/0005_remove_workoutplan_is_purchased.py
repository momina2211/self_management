# Generated by Django 3.2 on 2025-04-30 11:18

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('fitness', '0004_rename_is_purchasable_workoutplan_is_purchased'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='workoutplan',
            name='is_purchased',
        ),
    ]
