# Generated by Django 3.0.4 on 2020-05-01 07:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('SalesApp', '0026_auto_20200430_1728'),
    ]

    operations = [
        migrations.AddField(
            model_name='quote',
            name='inclusions_updated',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='quote',
            name='itinerary_updated',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='quote',
            name='quote_valid',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='quoteflightinfo',
            name='price',
            field=models.FloatField(default=0),
        ),
        migrations.AlterField(
            model_name='quotehotelinfo',
            name='price',
            field=models.FloatField(default=0),
        ),
        migrations.AlterField(
            model_name='quoteothersinfo',
            name='price',
            field=models.FloatField(default=0),
        ),
        migrations.AlterField(
            model_name='quotetransportinfo',
            name='price',
            field=models.FloatField(default=0),
        ),
    ]
