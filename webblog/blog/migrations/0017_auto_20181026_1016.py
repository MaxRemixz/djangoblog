# Generated by Django 2.1.1 on 2018-10-26 10:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0016_auto_20181026_1002'),
    ]

    operations = [
        migrations.AlterField(
            model_name='blog_articles',
            name='create_time',
            field=models.DateTimeField(default='2018-10-26 10:16:26', verbose_name='创建时间'),
        ),
        migrations.AlterField(
            model_name='comment',
            name='create_time',
            field=models.DateTimeField(default='2018-10-26 10:16:26', verbose_name='评论时间'),
        ),
        migrations.AlterField(
            model_name='friendship',
            name='create_time',
            field=models.DateTimeField(default='2018-10-26 10:16:26', verbose_name='创建时间'),
        ),
    ]
