# Generated by Django 3.0.4 on 2020-04-01 18:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('onlineStyle_App', '0005_remove_product_special'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='email',
            field=models.CharField(max_length=200, primary_key=True, serialize=False, unique=True),
        ),
    ]