# Generated by Django 2.1.2 on 2018-10-10 14:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0006_user_avatar_hash'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='avatar_hash',
            field=models.CharField(max_length=32),
        ),
    ]