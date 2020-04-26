# Generated by Django 3.0.4 on 2020-04-21 11:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('onlineStyle_App', '0040_delete_list'),
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=400, null=True)),
                ('status', models.IntegerField(choices=[(0, 'Not Avilable'), (1, 'Avilable')], default=0)),
            ],
        ),
    ]
