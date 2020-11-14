# Generated by Django 3.0.4 on 2020-05-30 10:41

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('ProfilesApp', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Traveler',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(blank=True, choices=[('MR', 'Mr'), ('MS', 'Ms'), ('DR', 'Dr')], max_length=10)),
                ('firstname', models.CharField(blank=True, max_length=100, null=True)),
                ('lastname', models.CharField(blank=True, max_length=100, null=True)),
                ('gender', models.CharField(choices=[('MALE', 'Male'), ('FEMALE', 'Female')], max_length=50)),
                ('dob', models.DateField(blank=True, null=True)),
                ('passport_num', models.CharField(blank=True, max_length=50, null=True)),
                ('place_of_issue', models.CharField(blank=True, max_length=50, null=True)),
                ('expiry_date', models.DateField(blank=True, null=True)),
                ('issue_Date', models.DateField(blank=True, null=True)),
                ('customer', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='ProfilesApp.Customer')),
            ],
        ),
    ]
