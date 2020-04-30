# Generated by Django 3.0.4 on 2020-04-26 07:19

from django.db import migrations, models
import django.db.models.deletion
import django_mysql.models


class Migration(migrations.Migration):

    dependencies = [
        ('ContentApp', '0002_auto_20200424_1437'),
        ('SalesApp', '0007_auto_20200426_1126'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='HotelsQuote',
            new_name='QuoteHotelInfo',
        ),
        migrations.RemoveField(
            model_name='quote',
            name='end_date',
        ),
        migrations.RemoveField(
            model_name='quote',
            name='hotels',
        ),
        migrations.RemoveField(
            model_name='quote',
            name='sightseeings',
        ),
        migrations.RemoveField(
            model_name='quote',
            name='start_date',
        ),
        migrations.RemoveField(
            model_name='quote',
            name='transfers',
        ),
        migrations.RemoveField(
            model_name='quotehotelinfo',
            name='quote_basics',
        ),
        migrations.AddField(
            model_name='quotehotelinfo',
            name='quote',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, to='SalesApp.Quote'),
        ),
        migrations.AlterField(
            model_name='quote',
            name='children',
            field=models.PositiveSmallIntegerField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='quote',
            name='children_age',
            field=django_mysql.models.ListCharField(models.IntegerField(), blank=True, max_length=20, null=True, size=None),
        ),
        migrations.AlterField(
            model_name='quote',
            name='cities',
            field=models.ManyToManyField(to='ContentApp.City'),
        ),
        migrations.AlterField(
            model_name='quote',
            name='destinations',
            field=models.ManyToManyField(to='ContentApp.Destination'),
        ),
        migrations.AlterField(
            model_name='quote',
            name='lead',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='SalesApp.Lead'),
        ),
        migrations.DeleteModel(
            name='QuoteBasics',
        ),
    ]