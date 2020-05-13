# Generated by Django 3.0.4 on 2020-05-05 13:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ContentApp', '0016_auto_20200505_1737'),
        ('SalesApp', '0037_auto_20200505_1908'),
    ]

    operations = [
        migrations.AlterField(
            model_name='inclusion',
            name='sightseeings',
            field=models.ManyToManyField(blank=True, null=True, to='ContentApp.Sightseeing'),
        ),
        migrations.AlterField(
            model_name='inclusion',
            name='transfers',
            field=models.ManyToManyField(blank=True, null=True, to='ContentApp.Transfer'),
        ),
        migrations.AlterField(
            model_name='inclusion',
            name='transports',
            field=models.ManyToManyField(blank=True, null=True, to='ContentApp.Transport'),
        ),
        migrations.AlterField(
            model_name='inclusion',
            name='visas',
            field=models.ManyToManyField(blank=True, null=True, to='ContentApp.Visa'),
        ),
    ]
