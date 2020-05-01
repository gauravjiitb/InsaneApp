# Generated by Django 3.0.4 on 2020-04-30 12:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ContentApp', '0004_auto_20200430_1729'),
    ]

    operations = [
        migrations.AlterField(
            model_name='sightseeing',
            name='adult_cutoff_age',
            field=models.PositiveSmallIntegerField(default=8),
        ),
        migrations.AlterField(
            model_name='sightseeing',
            name='child_cutoff_age',
            field=models.PositiveSmallIntegerField(default=2),
        ),
    ]
