# Generated by Django 3.0.4 on 2020-04-01 13:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('SalesApp', '0012_auto_20200401_1848'),
    ]

    operations = [
        migrations.AlterField(
            model_name='lead',
            name='trip_id',
            field=models.CharField(editable=False, max_length=10, unique=True),
        ),
    ]
