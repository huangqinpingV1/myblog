# Generated by Django 4.1.5 on 2023-02-22 04:15

import django.contrib.auth.models
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0002_alter_bloguser_managers'),
    ]

    operations = [
        migrations.AlterModelManagers(
            name='bloguser',
            managers=[
                ('objects', django.contrib.auth.models.UserManager()),
            ],
        ),
    ]