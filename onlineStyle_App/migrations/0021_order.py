# Generated by Django 3.0.4 on 2020-04-11 14:00

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('onlineStyle_App', '0020_auto_20200410_1141'),
    ]

    operations = [
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateTimeField(auto_now_add=True)),
                ('order', models.IntegerField(choices=[(1, 'canceled'), (2, 'complete'), (3, 'tracking')], default=3)),
                ('cart', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='onlineStyle_App.Cart')),
            ],
        ),
    ]
