import datetime
import json

from django.db import models
from django.urls import reverse
from django.db.models import F,Q

from django_mysql.models import ListCharField
from phonenumber_field.modelfields import PhoneNumberField

from ContentApp.managers import PricingManager

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
    destination = models.ForeignKey(Destination,related_name='Cities',on_delete=models.PROTECT,db_index=True)

    def __str__(self):
        return self.name

class Hotel(models.Model):
    name = models.CharField(max_length=255)
    city = models.ForeignKey(City,related_name='Hotels',on_delete=models.PROTECT,db_index=True)
    email = models.EmailField(blank=True)
    phone = PhoneNumberField(blank=True)

    def __str__(self):
        return '{} | {}'.format(self.name, self.city)


class Transport(models.Model):
    from_city = models.ForeignKey(City,related_name='Transports_From_City',on_delete=models.PROTECT)
    to_city = models.ForeignKey(City,related_name='Transports_To_City',on_delete=models.PROTECT)
    transport_class = models.CharField(max_length=50,choices=[('TRAIN','Train'),('BUS','Bus'),('FERRY','Ferry'),('TAXI','Taxi'),('CAR','Self Drive Car Rental')])
    transport_type =  models.CharField(max_length=50,choices=[('PRIVATE', 'Private'),('SHARED', 'Shared')],default='SHARED')
    duration = models.PositiveSmallIntegerField(blank=True,null=True) # in hours
    description = models.TextField(blank=True)
    remarks = models.CharField(max_length=255,blank=True)
    variable_pricing = models.BooleanField(default=False)


    def __str__(self):
        return '{} - {} | {}'.format(self.from_city, self.to_city,self.transport_class)


class Transfer(models.Model):
    city = models.ForeignKey(City,related_name='Transfers',on_delete=models.PROTECT,db_index=True)
    name = models.CharField(max_length=256)
    transfer_type = models.CharField(max_length=255,choices=[('PRIVATE', 'Private'),('SHARED', 'Shared')],default='SHARED')
    description = models.TextField()
    free = models.BooleanField(default=False)

    def __str__(self):
        return '{} | {}'.format(self.name, self.city.name)

class Sightseeing(models.Model):
    city = models.ForeignKey(City,related_name='Sightseeing',on_delete=models.PROTECT,db_index=True)
    name = models.CharField(max_length=255,unique=True)
    description = models.TextField()
    duration = models.PositiveSmallIntegerField(blank=True,null=True) # in hours
    tour_type =  models.CharField(max_length=255,choices=[('PRIVATE', 'With Private Transfers'),('SHARED', 'With Shared Transfers'),('NONE','Without Transfers')],default='SHARED')
    max_pax = models.PositiveSmallIntegerField(blank=True,null=True)
    remarks = models.CharField(max_length=255,blank=True)
    free = models.BooleanField(default=False)

    def __str__(self):
        return '{} | {}'.format(self.name, self.city.name)


class Visa(models.Model):
    name = models.CharField(max_length=255,unique=True)
    destinations = models.ManyToManyField(Destination,related_name='Visas')

    def __str__(self):
        return self.name

class Insurance(models.Model):
    insurer = models.CharField(max_length=255)
    duration = models.PositiveSmallIntegerField() # in Days
    destinations = models.ManyToManyField(Destination)
    coverage = models.PositiveIntegerField() # in USD

    def __str__(self):
        return '{} | {} USD | {} Days'.format(self.insurer, self.coverage, self.duration)

class Vendor(models.Model):
    name = models.CharField(max_length=255,unique=True)
    destinations = models.ManyToManyField(Destination,related_name='Vendors')
    email = models.EmailField(blank=True)
    phone = PhoneNumberField(blank=True)

    def __str__(self):
        return self.name


class Pricing(models.Model):
    package = models.ForeignKey('SalesApp.Package',on_delete=models.CASCADE,blank=True,null=True)
    inclusion = models.ForeignKey('SalesApp.Inclusion',on_delete=models.CASCADE,blank=True,null=True)
    transport = models.ForeignKey(Transport,on_delete=models.CASCADE,blank=True,null=True)
    transfer = models.ForeignKey(Transfer,on_delete=models.CASCADE,blank=True,null=True)
    sightseeing = models.ForeignKey(Sightseeing,on_delete=models.CASCADE,blank=True,null=True)
    visa = models.ForeignKey(Visa,on_delete=models.CASCADE,blank=True,null=True)
    insurance = models.ForeignKey(Insurance,on_delete=models.CASCADE,blank=True,null=True)

    name = models.CharField(max_length=100,blank=True)
    pricing_type = models.CharField(max_length=50,choices=[('FLAT', 'Flat pricing per adult / child'),('PAXWISE', 'Pricing by total number of pax')],default='FLAT')
    flat_adult_price = models.DecimalField(max_digits=8, decimal_places=2,blank=True,null=True)
    flat_child_price = models.DecimalField(max_digits=8, decimal_places=2,blank=True,null=True)
    adult_cutoff_age = models.PositiveSmallIntegerField(default=2)
    child_cutoff_age = models.PositiveSmallIntegerField(default=1)
    paxwise_max_pax_list = models.CharField(max_length=50,blank=True)
    paxwise_price_list = models.CharField(max_length=100,blank=True) # PRICES SHOULD BE MENTIONED FOR ALL PAX COMBINED

    valid = models.BooleanField(default=False)
    valid_from_date = models.DateField(default=datetime.date.today)
    valid_till_date = models.DateField(blank=True,null=True)

    objects = models.Manager()
    pricemanager = PricingManager()

    # def get_pricing(self,adults,children_ages):
    #     # CALCULATE THE TOTAL NUMBER OF CHILDREN
    #     children = 0
    #     if children_ages:
    #         children_age_list = children_ages.split(',')
    #         for i in range(len(children_age_list)):
    #             age = int(children_age_list[i])
    #             if age >= self.adult_cutoff_age:
    #                 adults += 1
    #             elif age >= self.child_cutoff_age:
    #                 children += 1
    #     total_pax = adults + children
    #
    #     # if self.season_pricing_bool:
    #     #     season_list = json.loads(self.season_cutoff_dates)
    #     #     season_list = list(map(lambda x: datetime.datetime.strptime(x,'%Y-%m-%d'),season_list)) # CONVERTING STRINGS TO DATES
    #     #     total_seasons = len(season_list) + 1
    #     #     y = [x for x in season_list if x > date]
    #     #     season_index = total_seasons - len(y)
    #     #     adult_price_factor = json.loads(self.season_adult_price_factors)[season_index]
    #     #     child_price_factor = json.loads(self.season_child_price_factors)[season_index]
    #
    #     if self.pricing_type == 'FLAT':
    #         price = (adults*flat_adult_price + children*flat_child_price)
    #     else:
    #         max_pax_list = self.paxwise_max_pax_list.split(',')
    #         price_list = self.paxwise_price_list.split(',')
    #         y = [x for x in max_pax_list if x > total_pax] # FIND ALL THE VEHICLES WITH CAPACITY MORE THAN GIVEN PAX
    #         if not y: # CHECK IF THE GIVEN PAX ARE MORE THAN THE BIGGEST VEHICLE SIZE, THEN DIVIDE THEM IN VEHICLES
    #             extra_pax = (total_pax % Y[-1])
    #             price = extra_pax*price_list[0] + (total_pax - extra_pax)*price_list[-1]
    #         else:
    #             a = y[0] # FIND THE MINIMUM VEHICLE WITH CAPACITY MORE THAN GIVEN PAX
    #             i = price_list.index(a)
    #             price = total_pax*price_list[i]
    #     return price
    #
