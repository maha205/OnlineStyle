# Generated by Django 3.0.4 on 2020-04-11 14:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('onlineStyle_App', '0024_auto_20200411_1747'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cart',
            name='order',
            field=models.IntegerField(choices=[(1, 'canceled'), (2, 'complete'), (3, 'tracking'), (0, 'None')], default=0),
        ),
    ]