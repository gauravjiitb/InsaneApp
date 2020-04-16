# Generated by Django 3.0.4 on 2020-04-12 08:22

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('ContentApp', '0001_initial'),
        ('AccountsApp', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='pendingpayment',
            name='proforma_invoice',
        ),
        migrations.AlterField(
            model_name='pendingpayment',
            name='vendor',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='PendingPayments', to='ContentApp.Vendor'),
        ),
        migrations.AlterField(
            model_name='transaction',
            name='remarks',
            field=models.CharField(blank=True, max_length=256),
        ),
        migrations.DeleteModel(
            name='ProformaInvoice',
        ),
    ]