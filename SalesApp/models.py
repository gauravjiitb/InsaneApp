from datetime import timedelta,date
import json
from decimal import Decimal

from django.db import models
from django.db.models import Model
from django.urls import reverse

from tinymce.models import HTMLField

from MarketingApp.models import LeadSource
from ProfilesApp.models import Customer,Staff
from ContentApp.models import (Destination, City, Transport, Hotel, Transfer, Sightseeing,
                                Visa, Insurance, Theme, Tag, Pricing)

#########################################
# HELPER FUNCTIONS

def get_trip_id():
    try:
        last_lead = Lead.objects.all().order_by('id').last()
        new_trip_id = "IN"+ str(17000+last_lead.id)
        return new_trip_id
    except:
        return 'IN170001'


#########################################


# Create your models here.

class Lead(models.Model):
    lead_status_choices = [
        ('NEW', 'New Enquiry'),
        ('QUOTED', 'Quoted'),
        ('BOOKED', 'Booked'),
        ('NOT_CONVERTED', 'Not Converted')
    ]
    customer = models.ForeignKey(Customer,related_name='Leads',on_delete=models.PROTECT)
    destinations = models.ManyToManyField(Destination,related_name='Leads')
    lead_source = models.ForeignKey(LeadSource,related_name='Leads',on_delete=models.PROTECT)
    id_at_lead_source = models.CharField(max_length=25,blank=True)
    lead_status = models.CharField(max_length=25,choices=lead_status_choices,default='NEW')
    remarks = models.TextField(blank=True)
    trip_id = models.CharField(max_length=10,editable=False,unique=True,default=get_trip_id)
    creation_date = models.DateField(auto_now=True)
    owner = models.ForeignKey(Staff,related_name='Leads',on_delete=models.PROTECT,blank=True,null=True)
    assigned_staff = models.ManyToManyField(Staff,related_name='AssignedLeads',blank=True)

    def get_absolute_url(self):
        return reverse("SalesApp:lead_detail",kwargs={'pk':self.pk})

    def __str__(self):
        lead_display_name =  '{} - {}'.format(self.trip_id, self.customer.user.name)
        return lead_display_name

class HotelGroup(models.Model):
    name = models.CharField(max_length=100)
    package = models.ForeignKey('SalesApp.Package',on_delete=models.CASCADE,blank=True,null=True)
    def __str__(self):
        return self.name

class Package(models.Model):
    type = models.CharField(max_length=20,choices=[('FIXED', 'Fixed Price Package'),('TEMPLATE', 'Custom Package Template')])
    title = models.CharField(max_length=100)
    themes = models.ManyToManyField(Theme)
    tags = models.ManyToManyField(Tag)
    starting_place = models.CharField(max_length=100)
    destinations = models.ManyToManyField(Destination)
    cities = models.ManyToManyField(City)
    duration = models.PositiveSmallIntegerField(blank=True,null=True)
    min_pax = models.PositiveSmallIntegerField(blank=True,null=True)
    itinerary = models.TextField(blank=True) # FORMAT-- [[transport-45,transfer-6,sightseeing-31],[sightseeing-56,transfer-12,..],[],...]

    package_valid = models.BooleanField(default=True)
    inclusions_updated = models.BooleanField(default=False)
    itinerary_updated = models.BooleanField(default=False)
    inclusions_exist = models.BooleanField(default=False)
    itinerary_exist = models.BooleanField(default=False)
    package_active = models.BooleanField(default=True)
    validity_start_date = models.DateField(default=date.today,blank=True,null=True)
    validity_end_date = models.DateField(blank=True,null=True)

    price = models.DecimalField(max_digits=8, decimal_places=2,blank=True,null=True)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse("SalesApp:package_detail",kwargs={'pk':self.pk})

    def get_daywise_itinerary(self):
        itinerary_objects_list = []
        itinerary = []
        objects = self.inclusion_set.filter(itinerary_inclusion=True)
        for i in range(self.duration):
            itinerary_objects_list.append(list(objects.filter(day=i+1).order_by('itinerary_order')))
        for day in itinerary_objects_list:
            day_plan = []
            for item in day:
                if item.item_type == '2_TRANSPORT':
                    day_plan.append(item.transport.description)
                elif item.item_type == '3_TRANSFER':
                    day_plan.append(item.transfer.description)
                elif item.item_type == '4_SIGHTSEEING':
                    day_plan.append(item.sightseeing.description)
                elif item.item_type == '7_OTHER':
                    day_plan.append(item.details)
            itinerary.append(day_plan)
        return itinerary


class Quote(models.Model):
    lead = models.ForeignKey(Lead,on_delete=models.PROTECT)
    themes = models.ManyToManyField(Theme)
    tags = models.ManyToManyField(Tag)
    adults = models.PositiveSmallIntegerField()
    children = models.PositiveSmallIntegerField(blank=True,null=True)
    children_age = models.CharField(max_length=100,blank=True)
    title = models.CharField(max_length=100,blank=True)
    name = models.CharField(max_length=100,blank=True)
    starting_place = models.CharField(max_length=100)
    destinations = models.ManyToManyField(Destination)
    cities = models.ManyToManyField(City)
    start_date = models.DateField()
    end_date = models.DateField()
    duration = models.PositiveSmallIntegerField(blank=True,null=True)
    manual_price = models.DecimalField(max_digits=8, decimal_places=2,default=0,blank=True,null=True)
    price = models.DecimalField(max_digits=8, decimal_places=2,default=0,blank=True,null=True)
    mark_up = models.DecimalField(max_digits=8, decimal_places=2,default=0)
    discount = models.DecimalField(max_digits=8, decimal_places=2,default=0)
    itinerary = models.TextField(blank=True) # FORMAT-- [[transport-45,transfer-6,sightseeing-31],[sightseeing-56,transfer-12,..],[],...]
    packages = models.ManyToManyField(Package)

    booked = models.BooleanField(default=False)
    quote_valid = models.BooleanField(default=False)
    price_valid = models.BooleanField(default=False)
    inclusions_updated = models.BooleanField(default=False)
    itinerary_updated = models.BooleanField(default=False)
    inclusions_exist = models.BooleanField(default=False)
    itinerary_exist = models.BooleanField(default=False)
    quote_active = models.BooleanField(default=True)
    inclusions_format = models.CharField(max_length=100,choices=[('FIXED','Fixed Inlusions'),('CUSTOM','Customized Inclusions'),('FLEXIBLE','Full Flexible Format')], default='CUSTOM')

    def __str__(self):
        return '{} | {}'.format(self.lead, self.title)

    def get_absolute_url(self):
        return reverse("SalesApp:quote_detail",kwargs={'pk':self.pk})

    def get_inclusions_price_list(self):
        adults = self.adults
        children_age = self.children_age
        auto_price = 0
        objects_price_list = []

        if self.inclusions_exist:
            for inclusion in self.inclusion_set.exclude(include=False):
                if inclusion.fixed_package_item:
                    objects_price_list.append([inclusion,None,False])
                elif inclusion.price:
                    objects_price_list.append([inclusion,inclusion.price,''])
                    auto_price += inclusion.price
                else:
                    date = self.start_date + timedelta(days=inclusion.day-1) if inclusion.day else self.start_date
                    if inclusion.item_type in ['0_FLIGHT','1_HOTEL']:
                        objects_price_list.append([inclusion,0,True])
                    elif inclusion.item_type in ['2_TRANSPORT','3_TRANSFER','4_SIGHTSEEING','5_VISA','6_INSURANCE']:
                        if inclusion.item_type == '2_TRANSPORT':
                            object = inclusion.transport
                        elif inclusion.item_type == '3_TRANSFER':
                            object = inclusion.transfer
                        elif inclusion.item_type == '4_SIGHTSEEING':
                            object = inclusion.sightseeing
                        elif inclusion.item_type == '5_VISA':
                                object = inclusion.visa
                        elif inclusion.item_type == '6_INSURANCE':
                                object = inclusion.insurance
                        p = Pricing.pricemanager.get_object_pricing(object=object,adults=adults,children_age=children_age,date=date)
                        error = True if p == 'Pricing Error' else False
                        objects_price_list.append([inclusion,p,error])
                        if p != 'Pricing Error':
                            auto_price += p
                    elif inclusion.item_type == '7_OTHER':
                        objects_price_list.append([inclusion,inclusion.price,False])
                        if inclusion.price:
                            auto_price += inclusion.price
                    elif inclusion.item_type == '8_EXCLUSION':
                        objects_price_list.append([inclusion,0,False])
        for package in self.packages.all():
            if package:
                p = Pricing.pricemanager.get_object_pricing(object=package,adults=adults,children_age=children_age,date=self.start_date)
                if p != 'Pricing Error':
                    auto_price += p
        return objects_price_list, auto_price

    def get_daywise_itinerary(self):
        itinerary_objects_list = []
        itinerary = []
        objects = self.inclusion_set.filter(itinerary_inclusion=True, include=True)
        for i in range(self.duration):
            itinerary_objects_list.append(list(objects.filter(day=i+1).order_by('itinerary_order')))
        for day in itinerary_objects_list:
            day_plan = []
            for item in day:
                if item.item_type == '2_TRANSPORT':
                    day_plan.append(item.transport.description)
                elif item.item_type == '3_TRANSFER':
                    day_plan.append(item.transfer.description)
                elif item.item_type == '4_SIGHTSEEING':
                    day_plan.append(item.sightseeing.description)
                elif item.item_type == '7_OTHER':
                    day_plan.append(item.details)
            itinerary.append(day_plan)
        return itinerary


class Inclusion(models.Model):
    item_type_choices = [('0_FLIGHT','Flight'),('1_HOTEL','Hotel'),('2_TRANSPORT','Transport'),('3_TRANSFER','Transfer'),('4_SIGHTSEEING','Sightseeing'),
                            ('5_VISA','Visa'),('6_INSURANCE','Insurance'),('7_OTHER','Other'),('8_EXCLUSION','Exclusion')]
    package = models.ForeignKey(Package,on_delete=models.CASCADE,blank=True,null=True)
    quote = models.ForeignKey(Quote,on_delete=models.CASCADE,blank=True,null=True)
    hotel_group = models.ForeignKey(HotelGroup,on_delete=models.CASCADE,blank=True,null=True)

    title = models.TextField(blank=True)
    item_type = models.CharField(max_length=50,choices=item_type_choices)
    other_type = models.CharField(max_length=50,choices=[('TRANSPORT','Transport'),('TRANSFER','Transfer'),('SIGHTSEEING','Sightseeing'),('OTHER','Other')],default='OTHER')
    day = models.PositiveSmallIntegerField(blank=True,null=True)
    nights = models.PositiveSmallIntegerField(blank=True,null=True)
    room_type = models.CharField(max_length=100,blank=True)
    airline = models.CharField(max_length=50,blank=True)
    name = models.CharField(max_length=100,blank=True)
    details = models.TextField(max_length=1000,blank=True)
    price = models.DecimalField(max_digits=8, decimal_places=2,blank=True,null=True)
    city = models.ForeignKey(City,on_delete=models.CASCADE,blank=True,null=True)

    transport = models.ForeignKey(Transport,on_delete=models.CASCADE,blank=True,null=True)
    hotel = models.ForeignKey(Hotel,on_delete=models.CASCADE,blank=True,null=True)
    transfer = models.ForeignKey(Transfer,on_delete=models.CASCADE,blank=True,null=True)
    sightseeing = models.ForeignKey(Sightseeing,on_delete=models.CASCADE,blank=True,null=True)
    visa = models.ForeignKey(Visa,on_delete=models.CASCADE,blank=True,null=True)
    insurance = models.ForeignKey(Insurance,on_delete=models.CASCADE,blank=True,null=True)

    itinerary_inclusion = models.BooleanField(default=False)
    itinerary_order = models.PositiveSmallIntegerField(blank=True,null=True)
    fixed_package_item = models.BooleanField(default=False)
    freeze = models.BooleanField(default=False)
    optional = models.BooleanField(default=False)
    include = models.BooleanField(default=True)

    def __str__(self):
        return self.title

#############################################################################
# DEPRECATED CODE
#############################################################################


    # def get_daywise_itinerary_objects(self):
    #     itinerary_objects_list = []
    #     if self.quote_itinerary:
    #         include_list = json.loads(self.itinerary)
    #         for day in include_list:
    #             object_list = []
    #             for item in day:
    #                 if item:
    #                     [object_type,id] = item.split('-')
    #                     if object_type == 'transfer':
    #                         object_list.append(Transfer.objects.get(id=id))
    #                     elif object_type == 'sightseeing':
    #                         object_list.append(Sightseeing.objects.get(id=id))
    #                     elif object_type == 'transport':
    #                         object_list.append(Transport.objects.get(id=id))
    #                     elif object_type == 'other':
    #                         object_list.append(Inclusion.objects.get(id=id))
    #             itinerary_objects_list.append(object_list)
    #     return itinerary_objects_list
    #
    # def get_quote_price_list(self):
    #     date = self.end_date
    #     adults = self.adults
    #     children_age = self.children_age
    #
    #     auto_price = 0
    #     objects_price_list = []
    #     if self.quote_inclusions:
    #         for inclusion in self.inclusion_set.all():
    #             if inclusion.item_type in ['FLIGHT','HOTEL','OTHER']:
    #                 object = inclusion
    #                 price = inclusion.price if not inclusion.fixed_package_item else None
    #                 error = False
    #                 objects_price_list.append([object,price,error])
    #                 if price and price != 'Pricing Error':
    #                     auto_price += price
    #             elif inclusion.item_type == 'VARIABLE_TRANSPORT':
    #                 object = inclusion.variable_transports
    #                 price = inclusion.price if not inclusion.fixed_package_item else None
    #                 error = False
    #                 objects_price_list.append([object,price,error])
    #                 if price and price != 'Pricing Error':
    #                     auto_price += price
    #             elif inclusion.item_type == 'INSURANCE':
    #                 object = inclusion.insurance
    #                 p = Pricing.pricemanager.get_object_pricing(object=object,adults=adults,children_age=children_age,date=date)
    #                 price = p if not inclusion.fixed_package_item else None
    #                 error = True if p == 'Pricing Error' else False
    #                 objects_price_list.append([object,price,error])
    #                 if price and price != 'Pricing Error':
    #                     auto_price += price
    #             elif inclusion.item_type in ['TRANSPORT','TRANSFER','SIGHTSEEING','VISA']:
    #                 if inclusion.item_type == 'TRANSPORT':
    #                     objects = inclusion.transports.all()
    #                 elif inclusion.item_type == 'TRANSFER':
    #                     objects = inclusion.transfers.all()
    #                 elif inclusion.item_type == 'SIGHTSEEING':
    #                     objects = inclusion.sightseeings.all()
    #                 elif inclusion.item_type == 'VISA':
    #                         objects = inclusion.visas.all()
    #                 for object in objects:
    #                     p = Pricing.pricemanager.get_object_pricing(object=object,adults=adults,children_age=children_age,date=date)
    #                     price = p if not inclusion.fixed_package_item else None
    #                     error = True if p == 'Pricing Error' else False
    #                     objects_price_list.append([object,price,error])
    #                     if price and price != 'Pricing Error':
    #                         auto_price += price
    #             elif inclusion.item_type == 'EXCLUSION':
    #                 objects_price_list.append([inclusion,0,False])
    #     self.price = auto_price + self.mark_up - self.discount
    #     self.save()
    #     return objects_price_list, auto_price
