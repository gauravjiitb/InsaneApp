from django.db import models
from phonenumber_field.modelfields import PhoneNumberField

# Create your models here.

class Destination(models.Model):
    region_choices = [
        ('WORLD', 'World'),
        ('IND', 'India'),
        ('EUR', 'Europe'),
        ('EASTEUR', 'Eastern Europe'),
        ('SA', 'South Asia'),
        ('NA', 'North Asia'),
        ('CA', 'Central Asia'),
        ('AFR', 'Africa'),
        ('AM', 'Americas'),
        ('ME', 'Middle East'),
        ('SCND', 'Scandinavia'),
        ('CRUISE', 'Cruise'),
    ]
    name = models.CharField(max_length=256,unique=True)
    description = models.TextField()
    region = models.CharField(max_length=256,choices=region_choices,default='WORLD')
    def __str__(self):
        return self.name


class City(models.Model):
    name = models.CharField(max_length=256,unique=True)
    destination = models.ForeignKey(Destination,related_name='Cities',on_delete=models.PROTECT)
    def __str__(self):
        return self.name

class Hotel(models.Model):
    name = models.CharField(max_length=256)
    city = models.ForeignKey(City,related_name='Hotels',on_delete=models.PROTECT)
    email = models.EmailField(blank=True)
    phone = PhoneNumberField(blank=True)
    def __str__(self):
        return self.name

class Transfer(models.Model):
    transfer_type_choices = [
        ('PRIVATE', 'Private'),
        ('SHARED', 'Shared'),
    ]
    city = models.ForeignKey(City,related_name='Transfers',on_delete=models.PROTECT)
    name = models.CharField(max_length=256)
    transfer_type = models.CharField(max_length=256,choices=transfer_type_choices,blank=True)
    def __str__(self):
        return self.name

class Sightseeing(models.Model):
    city = models.ForeignKey(City,related_name='Sightseeing',on_delete=models.PROTECT)
    name = models.CharField(max_length=256,unique=True)
    description = models.TextField()
    def __str__(self):
        return self.name

class Vendor(models.Model):
    name = models.CharField(max_length=256,unique=True)
    destinations = models.ManyToManyField(Destination,related_name='Vendors')
    email = models.EmailField(blank=True)
    phone = PhoneNumberField(blank=True)
    def __str__(self):
        return self.name
