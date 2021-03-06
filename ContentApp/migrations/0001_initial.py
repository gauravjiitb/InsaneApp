# Generated by Django 3.0.4 on 2020-04-01 05:33

from django.db import migrations, models
import django.db.models.deletion
import phonenumber_field.modelfields


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='City',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=256)),
            ],
        ),
        migrations.CreateModel(
            name='Destination',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=256)),
                ('description', models.TextField()),
            ],
        ),
        migrations.CreateModel(
            name='Vendor',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=256)),
                ('email', models.EmailField(blank=True, max_length=254)),
                ('phone', phonenumber_field.modelfields.PhoneNumberField(blank=True, max_length=128, region=None)),
                ('destination', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='Vendors', to='ContentApp.Destination')),
            ],
        ),
        migrations.CreateModel(
            name='Transfer',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=256)),
                ('transfer_type', models.CharField(blank=True, choices=[('PRIVATE', 'Private'), ('SHARED', 'Shared')], max_length=256)),
                ('city', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='Transfers', to='ContentApp.City')),
            ],
        ),
        migrations.CreateModel(
            name='Sightseeing',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=256)),
                ('description', models.TextField()),
                ('city', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='Sightseeing', to='ContentApp.City')),
            ],
        ),
        migrations.CreateModel(
            name='Hotel',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=256)),
                ('email', models.EmailField(blank=True, max_length=254)),
                ('phone', phonenumber_field.modelfields.PhoneNumberField(blank=True, max_length=128, region=None)),
                ('city', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='Hotels', to='ContentApp.City')),
            ],
        ),
        migrations.AddField(
            model_name='city',
            name='destination',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='Cities', to='ContentApp.Destination'),
        ),
    ]
