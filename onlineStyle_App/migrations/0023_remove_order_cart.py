# Generated by Django 3.0.4 on 2020-04-11 14:39

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('onlineStyle_App', '0022_auto_20200411_1719'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='order',
            name='cart',
        ),
    ]
