# Generated by Django 3.0.4 on 2020-04-11 18:42

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('onlineStyle_App', '0028_auto_20200411_2122'),
    ]

    operations = [
        migrations.RenameField(
            model_name='order',
            old_name='cart',
            new_name='carts',
        ),
    ]