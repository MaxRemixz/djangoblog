# Generated by Django 2.1.1 on 2018-10-28 10:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0018_auto_20181026_1103'),
    ]

    operations = [
        migrations.AlterField(
            model_name='comment',
            name='disabled',
            field=models.BooleanField(default=False),
        ),
    ]