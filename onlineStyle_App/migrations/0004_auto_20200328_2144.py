# Generated by Django 3.0.4 on 2020-03-28 18:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('onlineStyle_App', '0003_product'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='special',
            field=models.CharField(max_length=200, null=True),
        ),
        migrations.AlterField(
            model_name='product',
            name='title',
            field=models.CharField(max_length=200),
        ),
    ]