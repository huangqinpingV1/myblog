# Generated by Django 4.1.5 on 2023-02-17 07:04

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Links',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=30, verbose_name='链接名称')),
                ('link', models.URLField(verbose_name='链接地址')),
                ('sequence', models.IntegerField(unique=True, verbose_name='排序')),
                ('created_time', models.DateTimeField(auto_now_add=True, verbose_name='创建时间')),
                ('last_mod_time', models.DateTimeField(auto_now=True, verbose_name='修改时间')),
            ],
            options={
                'verbose_name': '友情链接',
                'verbose_name_plural': '友情链接',
                'ordering': ['sequence'],
            },
        ),
        migrations.AddField(
            model_name='article',
            name='comment_status',
            field=models.CharField(choices=[('o', '打开'), ('c', '关闭')], default='c', max_length=1, verbose_name='评论状态'),
        ),
        migrations.AddField(
            model_name='category',
            name='parent_category',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='blog.category', verbose_name='父级分类'),
        ),
        migrations.AlterField(
            model_name='article',
            name='status',
            field=models.CharField(choices=[('d', '草稿'), ('p', '发表')], default='o', max_length=1, verbose_name='文章状态'),
        ),
        migrations.AlterField(
            model_name='article',
            name='summary',
            field=models.CharField(blank=True, help_text='可选，若为空将摘取正文的前300个字符。', max_length=200, verbose_name='摘要'),
        ),
    ]
