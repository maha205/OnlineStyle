# Generated by Django 3.0.4 on 2020-04-11 14:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('onlineStyle_App', '0025_auto_20200411_1748'),
    ]

    operations = [
        migrations.AddField(
            model_name='cart',
            name='date',
            field=models.DateTimeField(auto_now=True),
        ),
    ]