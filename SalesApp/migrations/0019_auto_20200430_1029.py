# Generated by Django 3.0.4 on 2020-04-30 04:59

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('ContentApp', '0003_auto_20200427_1518'),
        ('SalesApp', '0018_auto_20200428_1710'),
    ]

    operations = [
        migrations.AlterField(
            model_name='quoteinsuranceinfo',
            name='insurance',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, to='ContentApp.Insurance'),
        ),
        migrations.AlterField(
            model_name='quoteitineraryinfo',
            name='ordering',
            field=models.CharField(blank=True, max_length=255),
        ),
        migrations.CreateModel(
            name='QuoteTransportInfo',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('type', models.CharField(choices=[('TRAIN', 'Train'), ('BUS', 'Bus'), ('FERRY', 'Ferry'), ('TAXI', 'Taxi')], max_length=100)),
                ('date', models.DateField()),
                ('details', models.CharField(max_length=255)),
                ('price', models.FloatField()),
                ('quote', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='SalesApp.Quote')),
            ],
        ),
        migrations.CreateModel(
            name='QuoteOthersInfo',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('description', models.TextField(blank=True, max_length=1000)),
                ('date', models.DateField(blank=True)),
                ('price', models.FloatField(blank=True, null=True)),
                ('quote', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='SalesApp.Quote')),
            ],
        ),
        migrations.CreateModel(
            name='QuoteFlightInfo',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('airline', models.CharField(blank=True, max_length=255)),
                ('details', models.TextField(max_length=1000)),
                ('remarks', models.CharField(blank=True, max_length=255)),
                ('price', models.FloatField()),
                ('quote', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='SalesApp.Quote')),
            ],
        ),
    ]