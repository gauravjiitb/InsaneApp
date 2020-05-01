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
    adult_cutoff_age = models.PositiveSmallIntegerField(default=8)
    child_cutoff_age = models.PositiveSmallIntegerField(default=2)
    duration = models.PositiveSmallIntegerField(blank=True,null=True) # in hours
    tour_type = [('PRIVATE', 'With Private Transfers'),('SHARED', 'With Shared Transfers'),('NONE','Without Transfers')]
    max_pax = models.PositiveSmallIntegerField(blank=True,null=True)
    remarks = models.CharField(max_length=255,blank=True)

    def __str__(self):
        return '{} | {}'.format(self.name, self.city)

    def get_pricing(self,adults,children_ages):
        children = 0
        if children_ages:
            children_age_list = list(children_ages.split(","))
            for i in range(len(children_age_list)):
                age = int(children_age_list[i])
                if age >= self.adult_cutoff_age:
                    adults += 1
                elif age >= self.child_cutoff_age:
                    children += 1
        total_pax = adults + children
        if not self.max_pax:
            return (adults*self.adult_price + children*self.child_price)
        else:
            extra_pax = (total_pax % self.max_pax)
            children = children - extra_pax
            return (adults*self.adult_price + children*self.child_price + self.max_pax*self.adult_price)

class Visa(models.Model):
    name = models.CharField(max_length=255,unique=True)
    destinations = models.ManyToManyField(Destination,related_name='Visas')
    adult_price = models.FloatField()
    child_price = models.FloatField()
    adult_cutoff_age = models.PositiveSmallIntegerField(default=3)
    child_cutoff_age = models.PositiveSmallIntegerField(default=0)

    def __str__(self):
        return self.name

    def get_pricing(self,adults,children_ages):
        children = 0
        if children_ages:
            children_age_list = list(children_ages.split(","))
            for i in range(len(children_age_list)):
                age = int(children_age_list[i])
                if age >= self.adult_cutoff_age:
                    adults += 1
                elif age >= self.child_cutoff_age:
                    children += 1
        return (adults*self.adult_price + children*self.child_price)


class Insurance(models.Model):
    insurer = models.CharField(max_length=255)
    duration = models.PositiveSmallIntegerField() # in Days
    destinations = models.ManyToManyField(Destination,related_name='Insurances')
    coverage = models.PositiveIntegerField() # in USD
    price = models.FloatField()

    def __str__(self):
        return '{} | {} USD | {} Days'.format(self.insurer, self.coverage, self.duration)

class Vendor(models.Model):
    name = models.CharField(max_length=255,unique=True)
    destinations = models.ManyToManyField(Destination,related_name='Vendors')
    email = models.EmailField(blank=True)
    phone = PhoneNumberField(blank=True)

    def __str__(self):
        return self.name
