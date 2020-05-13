# Generated by Django 3.0.4 on 2020-05-08 14:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ContentApp', '0023_auto_20200508_1525'),
        ('SalesApp', '0045_auto_20200508_1926'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='inclusion',
            name='variable_transports',
        ),
        migrations.AddField(
            model_name='inclusion',
            name='variable_transports',
            field=models.ManyToManyField(blank=True, related_name='Variable_Inclusions', to='ContentApp.Transport'),
        ),
    ]
