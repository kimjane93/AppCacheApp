# Generated by Django 3.1.6 on 2021-02-03 23:54

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('main_app', '0005_app_build_stat'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='app',
            name='build_stat',
        ),
    ]
