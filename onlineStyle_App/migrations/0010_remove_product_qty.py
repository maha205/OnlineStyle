# Generated by Django 3.0.4 on 2020-04-04 15:00

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('onlineStyle_App', '0009_auto_20200404_1757'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='product',
            name='qty',
        ),
    ]
