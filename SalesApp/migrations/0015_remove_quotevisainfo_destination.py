# Generated by Django 3.0.4 on 2020-04-27 10:06

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('SalesApp', '0014_quoteinsuranceinfo_quotevisainfo'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='quotevisainfo',
            name='destination',
        ),
    ]