# Generated by Django 3.0.4 on 2020-04-14 04:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('SalesApp', '0019_auto_20200402_1554'),
    ]

    operations = [
        migrations.AlterField(
            model_name='lead',
            name='trip_id',
            field=models.CharField(default='IN153F7', editable=False, max_length=10, unique=True),
        ),
    ]
