# Generated by Django 3.0.4 on 2020-04-21 11:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('onlineStyle_App', '0042_category_products'),
    ]

    operations = [
        migrations.AlterField(
            model_name='category',
            name='name',
            field=models.CharField(max_length=400, null=True, unique=True),
        ),
    ]
