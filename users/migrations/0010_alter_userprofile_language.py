# Generated by Django 5.2 on 2025-04-28 07:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0009_alter_language_id_alter_userprofile_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userprofile',
            name='language',
            field=models.ManyToManyField(blank=True, to='users.language'),
        ),
    ]
