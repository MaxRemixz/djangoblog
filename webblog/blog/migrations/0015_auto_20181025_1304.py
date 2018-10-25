# Generated by Django 2.1.1 on 2018-10-25 13:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0014_auto_20181025_1132'),
    ]

    operations = [
        migrations.AlterField(
            model_name='blog_articles',
            name='create_time',
            field=models.DateTimeField(default='2018-10-25 13:01:39', verbose_name='创建时间'),
        ),
        migrations.AlterField(
            model_name='comment',
            name='create_time',
            field=models.DateTimeField(default='2018-10-25 13:01:39', verbose_name='评论时间'),
        ),
        migrations.AlterField(
            model_name='comment',
            name='disabled',
            field=models.BooleanField(default=True),
        ),
        migrations.AlterField(
            model_name='friendship',
            name='create_time',
            field=models.DateTimeField(default='2018-10-25 13:01:39', verbose_name='创建时间'),
        ),
    ]