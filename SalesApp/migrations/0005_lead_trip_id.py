# Generated by Django 3.0.4 on 2020-03-26 13:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('SalesApp', '0004_remove_lead_trip_id'),
    ]

    operations = [
        migrations.AddField(
            model_name='lead',
            name='trip_id',
            field=models.CharField(default='IN17000', editable=False, max_length=256),
            preserve_default=False,
        ),
    ]
