# Generated by Django 3.0.4 on 2020-05-02 11:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ContentApp', '0007_auto_20200430_1817'),
    ]

    operations = [
        migrations.AddField(
            model_name='sightseeing',
            name='tour_type',
            field=models.CharField(choices=[('PRIVATE', 'With Private Transfers'), ('SHARED', 'With Shared Transfers'), ('NONE', 'Without Transfers')], default='SHARED', max_length=255),
        ),
    ]