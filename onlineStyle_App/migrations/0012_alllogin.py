# Generated by Django 3.0.4 on 2020-04-04 22:25

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('onlineStyle_App', '0011_cart'),
    ]

    operations = [
        migrations.CreateModel(
            name='AllLogin',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateTimeField(auto_now_add=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='onlineStyle_App.Person')),
            ],
        ),
    ]
