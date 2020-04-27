from django.db import models

from django_mysql.models import JSONField, Model, DynamicField
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
    name = models.CharField(max_length=255,unique=True)
    description = models.TextField()
    region = models.CharField(max_length=256,choices=region_choices,default='WORLD')
    def __str__(self):
        return self.name


class City(models.Model):
    name = models.CharField(max_length=255,unique=True)
    destination = models.ForeignKey(Destination,related_name='Cities',on_delete=models.PROTECT)

    def __str__(self):
        return self.name

class Hotel(Model):
    name = models.CharField(max_length=255)
    city = models.ForeignKey(City,related_name='Hotels',on_delete=models.PROTECT)
    email = models.EmailField(blank=True)
    phone = PhoneNumberField(blank=True)

    def __str__(self):
        return '{} | {}'.format(self.name, self.city)

class Transfer(models.Model):
    transfer_type_choices = [('PRIVATE', 'Private'),('SHARED', 'Shared')]

    city = models.ForeignKey(City,related_name='Transfers',on_delete=models.PROTECT)
    name = models.CharField(max_length=256)
    transfer_type = models.CharField(max_length=255,choices=transfer_type_choices,blank=True)
    description = models.TextField()
    max_pax = models.PositiveSmallIntegerField()
    price = models.FloatField()
    # pricing = DyanmicField() # Format--- (options = [ {'max_pax':??, 'price':??}, {'max_pax':??, 'price':??}, ...])

    # class Meta:
    #     constraints = [models.UniqueConstraint(fields=['city', 'name','transfer_type','max_pax'], name='unique_transfer_in_city')]

    def __str__(self):
        return '{} | {} | {} pax'.format(self.name, self.transfer_type, self.max_pax)

class Sightseeing(models.Model):
    city = models.ForeignKey(City,related_name='Sightseeing',on_delete=models.PROTECT)
    name = models.CharField(max_length=255,unique=True)
    description = models.TextField()
    adult_price = models.FloatField()
    child_price = models.FloatField()
    duration = models.PositiveSmallIntegerField(blank=True,null=True) # in hours
    remarks = models.CharField(max_length=255,blank=True)

    def __str__(self):
        return '{} | {}'.format(self.name, self.city)

class Visa(models.Model):
    name = models.CharField(max_length=255,unique=True)
    destination = models.ManyToManyField(Destination,related_name='Visas')
    adult_price = models.FloatField()
    child_price = models.FloatField()

class Insurance(models.Model):
    name = models.CharField(max_length=255,unique=True)
    duration = models.PositiveSmallIntegerField() # in Days
    coverage = models.IntegerField() # in USD
    price = models.FloatField()

class Vendor(models.Model):
    name = models.CharField(max_length=255,unique=True)
    destinations = models.ManyToManyField(Destination,related_name='Vendors')
    email = models.EmailField(blank=True)
    phone = PhoneNumberField(blank=True)

    def __str__(self):
        return self.name
