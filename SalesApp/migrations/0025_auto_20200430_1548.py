# Generated by Django 3.0.4 on 2020-04-30 10:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('SalesApp', '0024_auto_20200430_1544'),
    ]

    operations = [
        migrations.AlterField(
            model_name='quote',
            name='price',
            field=models.FloatField(blank=True, default=0, null=True),
        ),
    ]