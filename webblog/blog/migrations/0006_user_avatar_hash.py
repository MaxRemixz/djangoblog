# Generated by Django 2.1.2 on 2018-10-10 14:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0005_auto_20181007_1827'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='avatar_hash',
            field=models.CharField(default='abc', max_length=32),
        ),
    ]