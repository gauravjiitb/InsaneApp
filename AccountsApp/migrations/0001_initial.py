# Generated by Django 3.0.4 on 2020-04-24 05:20

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Account',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255, unique=True)),
                ('detail', models.TextField(blank=True)),
            ],
        ),
        migrations.CreateModel(
            name='PendingPayment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField()),
                ('amount', models.DecimalField(decimal_places=2, max_digits=19)),
                ('inout_type', models.CharField(choices=[('DR', 'Debit'), ('CR', 'Credit')], max_length=25)),
            ],
        ),
        migrations.CreateModel(
            name='Transaction',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField()),
                ('transaction_ref', models.CharField(max_length=256)),
                ('amount', models.DecimalField(decimal_places=2, max_digits=19)),
                ('reference_number', models.CharField(blank=True, max_length=256)),
                ('description', models.TextField()),
                ('inout_type', models.CharField(choices=[('DR', 'Debit'), ('CR', 'Credit')], max_length=25)),
                ('balance', models.DecimalField(decimal_places=2, max_digits=19)),
                ('remarks', models.CharField(blank=True, max_length=256)),
                ('reconcile_details', models.CharField(blank=True, max_length=500)),
                ('reconcile_status_bool', models.BooleanField(default=False, editable=False)),
            ],
            options={
                'ordering': ['date'],
            },
        ),
        migrations.CreateModel(
            name='TransactionHead',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255, unique=True)),
                ('trip_bool', models.BooleanField()),
            ],
        ),
        migrations.CreateModel(
            name='TripPayment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField(default=datetime.date.today)),
                ('amount', models.DecimalField(decimal_places=2, max_digits=19)),
                ('inout_type', models.CharField(choices=[('DR', 'Debit'), ('CR', 'Credit')], max_length=25)),
            ],
        ),
        migrations.CreateModel(
            name='TripPaymentHead',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255, unique=True)),
                ('type', models.CharField(choices=[('CUSTOMER', 'Customer'), ('VENDOR', 'Vendor')], default='VENDOR', max_length=25)),
            ],
        ),
    ]
