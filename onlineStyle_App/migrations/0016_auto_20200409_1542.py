# Generated by Django 3.0.4 on 2020-04-09 12:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('onlineStyle_App', '0015_auto_20200409_1531'),
    ]

    operations = [
        migrations.AlterField(
            model_name='sale',
            name='sale',
            field=models.IntegerField(choices=[(0, 'None'), (50, '1+1'), (33, '2+1'), (25, '3+1'), (25, '1+1/2')], default=0),
        ),
    ]