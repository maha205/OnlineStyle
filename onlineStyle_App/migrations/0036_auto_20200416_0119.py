# Generated by Django 3.0.4 on 2020-04-15 22:19

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('onlineStyle_App', '0035_person_club_card'),
    ]

    operations = [
        migrations.RenameField(
            model_name='order',
            old_name='order',
            new_name='status',
        ),
    ]