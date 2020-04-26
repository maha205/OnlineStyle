# Generated by Django 3.0.4 on 2020-04-04 21:26

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('onlineStyle_App', '0010_remove_product_qty'),
    ]

    operations = [
        migrations.CreateModel(
            name='Cart',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('qty_small', models.IntegerField(default=0)),
                ('qty_medium', models.IntegerField(default=0)),
                ('qty_large', models.IntegerField(default=0)),
                ('qty_xtraLarge', models.IntegerField(default=0)),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='onlineStyle_App.Product')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='onlineStyle_App.Person')),
            ],
        ),
    ]
