# Generated by Django 3.0.4 on 2020-04-28 04:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('SalesApp', '0015_remove_quotevisainfo_destination'),
    ]

    operations = [
        migrations.AddField(
            model_name='quote',
            name='end_date',
            field=models.DateField(default='2020-04-29'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='quote',
            name='start_date',
            field=models.DateField(default='2020-04-30'),
            preserve_default=False,
        ),
    ]
