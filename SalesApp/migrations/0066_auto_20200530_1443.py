# Generated by Django 3.0.4 on 2020-05-30 09:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('SalesApp', '0065_quote_price_valid'),
    ]

    operations = [
        migrations.AddField(
            model_name='quote',
            name='name',
            field=models.CharField(blank=True, max_length=100),
        ),
        migrations.AlterField(
            model_name='quote',
            name='title',
            field=models.CharField(blank=True, max_length=100),
        ),
    ]