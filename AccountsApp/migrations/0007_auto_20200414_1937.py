# Generated by Django 3.0.4 on 2020-04-14 14:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('AccountsApp', '0006_auto_20200414_1521'),
    ]

    operations = [
        migrations.AlterField(
            model_name='transaction',
            name='remarks',
            field=models.CharField(blank=True, max_length=256, null=True),
        ),
    ]