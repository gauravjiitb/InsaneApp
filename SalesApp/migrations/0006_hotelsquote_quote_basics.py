# Generated by Django 3.0.4 on 2020-04-26 05:30

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('SalesApp', '0005_auto_20200426_1004'),
    ]

    operations = [
        migrations.AddField(
            model_name='hotelsquote',
            name='quote_basics',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, to='SalesApp.QuoteBasics'),
        ),
    ]
