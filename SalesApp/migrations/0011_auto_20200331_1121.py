# Generated by Django 3.0.4 on 2020-03-31 05:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('SalesApp', '0010_auto_20200331_1054'),
    ]

    operations = [
        migrations.AlterField(
            model_name='lead',
            name='trip_id',
            field=models.CharField(default='IN9B39E', editable=False, max_length=10, unique=True),
        ),
    ]
