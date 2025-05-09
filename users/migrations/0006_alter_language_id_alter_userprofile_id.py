# Generated by Django 5.2 on 2025-04-24 07:24

import uuid
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0005_alter_language_id_alter_userprofile_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='language',
            name='id',
            field=models.UUIDField(default=uuid.UUID('6ec53aeb-e4be-480d-b2b8-2327d70d31e4'), editable=False, primary_key=True, serialize=False),
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='id',
            field=models.UUIDField(default=uuid.UUID('6ec53aeb-e4be-480d-b2b8-2327d70d31e4'), editable=False, primary_key=True, serialize=False),
        ),
    ]
