# Generated by Django 3.0.4 on 2020-04-02 11:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('onlineStyle_App', '0006_auto_20200401_2109'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='role',
            field=models.IntegerField(choices=[(1, 'user'), (2, 'admin')], default=1),
        ),
    ]