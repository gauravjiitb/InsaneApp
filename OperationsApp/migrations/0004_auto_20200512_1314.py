# Generated by Django 3.0.4 on 2020-05-12 07:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ContentApp', '0023_auto_20200508_1525'),
        ('OperationsApp', '0003_auto_20200512_1312'),
    ]

    operations = [
        migrations.AlterField(
            model_name='booking',
            name='booked_destinations',
            field=models.ManyToManyField(blank=True, null=True, related_name='Bookings', to='ContentApp.Destination'),
        ),
        migrations.AlterField(
            model_name='booking',
            name='travel_date',
            field=models.DateField(blank=True, null=True),
        ),
    ]
