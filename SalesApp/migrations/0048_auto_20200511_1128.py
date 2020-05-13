# Generated by Django 3.0.4 on 2020-05-11 05:58

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('SalesApp', '0047_auto_20200509_1304'),
    ]

    operations = [
        migrations.RenameField(
            model_name='inclusion',
            old_name='package_item',
            new_name='fixed_package_item',
        ),
        migrations.AddField(
            model_name='inclusion',
            name='nights',
            field=models.PositiveSmallIntegerField(blank=True, null=True),
        ),
        migrations.RemoveField(
            model_name='package',
            name='hotel_options',
        ),
        migrations.CreateModel(
            name='HotelGroup',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('inclusions', models.ManyToManyField(to='SalesApp.Inclusion')),
            ],
        ),
        migrations.AddField(
            model_name='inclusion',
            name='hotel_group',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='SalesApp.HotelGroup'),
        ),
        migrations.AddField(
            model_name='package',
            name='hotel_options',
            field=models.ManyToManyField(to='SalesApp.HotelGroup'),
        ),
    ]