# Generated by Django 3.0.4 on 2020-05-03 12:57

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('ContentApp', '0010_auto_20200503_1426'),
    ]

    operations = [
        migrations.AddField(
            model_name='fpitem',
            name='fixed_package',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, to='ContentApp.FixedPackage'),
        ),
        migrations.AlterField(
            model_name='fpitem',
            name='freeze_day',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='fpitem',
            name='freeze_inclusion',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='fpitem',
            name='name',
            field=models.CharField(blank=True, max_length=100),
        ),
    ]
