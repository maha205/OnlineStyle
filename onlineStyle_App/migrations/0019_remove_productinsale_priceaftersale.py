# Generated by Django 3.0.4 on 2020-04-10 07:04

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('onlineStyle_App', '0018_auto_20200409_1640'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='productinsale',
            name='priceAfterSale',
        ),
    ]
