# Generated by Django 3.0.4 on 2020-04-13 09:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('onlineStyle_App', '0033_delete_freeshipping'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='order',
            field=models.IntegerField(choices=[(2, 'tracking'), (1, 'complete')], default=2),
        ),
    ]
