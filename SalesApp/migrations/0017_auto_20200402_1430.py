# Generated by Django 3.0.4 on 2020-04-02 09:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('SalesApp', '0016_auto_20200402_1427'),
    ]

    operations = [
        migrations.AlterField(
            model_name='lead',
            name='trip_id',
            field=models.CharField(default='INF7256', editable=False, max_length=10, unique=True),
        ),
    ]
