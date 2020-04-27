# Generated by Django 3.0.4 on 2020-04-24 05:20

import SalesApp.models
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('MarketingApp', '0001_initial'),
        ('ContentApp', '0001_initial'),
        ('ProfilesApp', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Lead',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('id_at_lead_source', models.CharField(blank=True, max_length=25)),
                ('lead_status', models.CharField(choices=[('NEW', 'New Enquiry'), ('QUOTED', 'Quoted'), ('BOOKED', 'Booked')], default='NEW', max_length=25)),
                ('remarks', models.TextField(blank=True)),
                ('trip_id', models.CharField(default=SalesApp.models.get_trip_id, editable=False, max_length=10, unique=True)),
                ('creation_date', models.DateField(auto_now=True)),
                ('assigned_staff', models.ManyToManyField(blank=True, related_name='AssignedLeads', to='ProfilesApp.Staff')),
                ('customer', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='Leads', to='ProfilesApp.Customer')),
                ('destinations', models.ManyToManyField(related_name='Leads', to='ContentApp.Destination')),
                ('lead_source', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='Leads', to='MarketingApp.LeadSource')),
                ('owner', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='Leads', to='ProfilesApp.Staff')),
            ],
        ),
    ]
