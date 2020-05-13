# Generated by Django 3.0.4 on 2020-05-11 10:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('SalesApp', '0050_remove_hotelgroup_inclusions'),
    ]

    operations = [
        migrations.AlterField(
            model_name='package',
            name='package_valid',
            field=models.BooleanField(default=True),
        ),
        migrations.AlterField(
            model_name='package',
            name='validity_end_date',
            field=models.DateField(blank=True, null=True),
        ),
    ]