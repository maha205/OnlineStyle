# Generated by Django 3.0.4 on 2020-04-22 15:36

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('onlineStyle_App', '0045_product_category_name'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='product',
            name='category_name',
        ),
    ]
