# Generated by Django 4.2.3 on 2023-07-23 17:10

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0003_profile_username'),
    ]

    operations = [
        migrations.RenameField(
            model_name='profile',
            old_name='short_into',
            new_name='short_intro',
        ),
    ]
