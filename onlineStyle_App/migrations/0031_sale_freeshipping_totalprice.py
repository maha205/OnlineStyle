# Generated by Django 3.0.4 on 2020-04-12 10:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('onlineStyle_App', '0030_auto_20200411_2148'),
    ]

    operations = [
        migrations.AddField(
            model_name='sale',
            name='FreeShipping_totalPrice',
            field=models.IntegerField(default=0),
        ),
    ]
