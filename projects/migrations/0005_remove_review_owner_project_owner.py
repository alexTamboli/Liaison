# Generated by Django 4.2.3 on 2023-07-23 16:57

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0003_profile_username'),
        ('projects', '0004_review_owner'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='review',
            name='owner',
        ),
        migrations.AddField(
            model_name='project',
            name='owner',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='users.profile'),
        ),
    ]