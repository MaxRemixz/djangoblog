# Generated by Django 2.1.2 on 2018-10-07 10:27

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0004_auto_20181006_2118'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Articles',
            new_name='Blog_Articles',
        ),
        migrations.AlterModelManagers(
            name='user',
            managers=[
            ],
        ),
    ]
