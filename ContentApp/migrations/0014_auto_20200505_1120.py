# Generated by Django 3.0.4 on 2020-05-05 05:50

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('ContentApp', '0013_auto_20200504_1708'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='transport',
            name='detail',
        ),
        migrations.RemoveField(
            model_name='transport',
            name='from_destination',
        ),
        migrations.RemoveField(
            model_name='transport',
            name='to_destination',
        ),
    ]
