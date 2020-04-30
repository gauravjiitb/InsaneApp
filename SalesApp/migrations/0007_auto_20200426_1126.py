# Generated by Django 3.0.4 on 2020-04-26 05:56

from django.db import migrations, models
import django_mysql.models


class Migration(migrations.Migration):

    dependencies = [
        ('SalesApp', '0006_hotelsquote_quote_basics'),
    ]

    operations = [
        migrations.AlterField(
            model_name='quotebasics',
            name='children',
            field=models.PositiveSmallIntegerField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='quotebasics',
            name='children_age',
            field=django_mysql.models.ListCharField(models.IntegerField(), blank=True, max_length=20, null=True, size=None),
        ),
    ]