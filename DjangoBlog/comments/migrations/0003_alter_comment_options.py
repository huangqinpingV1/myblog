# Generated by Django 4.1.7 on 2023-05-18 08:51

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('comments', '0002_alter_comment_body'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='comment',
            options={'get_latest_by': 'created_time', 'ordering': ['created_time'], 'verbose_name': '评论', 'verbose_name_plural': '评论'},
        ),
    ]