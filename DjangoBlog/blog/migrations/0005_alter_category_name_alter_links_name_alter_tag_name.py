# Generated by Django 4.1.5 on 2023-04-04 06:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0004_remove_article_wordpress_id_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='category',
            name='name',
            field=models.CharField(max_length=30, unique=True, verbose_name='分类名'),
        ),
        migrations.AlterField(
            model_name='links',
            name='name',
            field=models.CharField(max_length=30, unique=True, verbose_name='链接名称'),
        ),
        migrations.AlterField(
            model_name='tag',
            name='name',
            field=models.CharField(max_length=30, unique=True, verbose_name='标签名'),
        ),
    ]
