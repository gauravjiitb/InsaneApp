# Generated by Django 3.0.4 on 2020-04-21 11:44

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('ProfilesApp', '0001_initial'),
        ('OperationsApp', '0001_initial'),
        ('SalesApp', '0001_initial'),
        ('ContentApp', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='booking',
            name='assigned_staff',
            field=models.ManyToManyField(blank=True, related_name='Bookings', to='ProfilesApp.Staff'),
        ),
        migrations.AddField(
            model_name='booking',
            name='booked_destinations',
            field=models.ManyToManyField(related_name='Bookings', to='ContentApp.Destination'),
        ),
        migrations.AddField(
            model_name='booking',
            name='lead',
            field=models.OneToOneField(on_delete=django.db.models.deletion.PROTECT, related_name='Booking', to='SalesApp.Lead'),
        ),
    ]