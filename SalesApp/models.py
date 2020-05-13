import datetime
import json
from decimal import Decimal

from django.db import models
from django.db.models import Model
from django.urls import reverse

from tinymce.models import HTMLField

from MarketingApp.models import LeadSource
from ProfilesApp.models import Customer,Staff
from ContentApp.models import Destination,City,Transport,Hotel,Transfer,Sightseeing,Visa,Insurance, Pricing

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
        ('BOOKED', 'Booked')
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
    starting_place = models.CharField(max_length=100)
    destinations = models.ManyToManyField(Destination)
    cities = models.ManyToManyField(City)
    duration = models.PositiveSmallIntegerField(blank=True,null=True)
    min_pax = models.PositiveSmallIntegerField(blank=True,null=True)
    itinerary = models.TextField(blank=True) # FORMAT-- [[transport-45,transfer-6,sightseeing-31],[sightseeing-56,transfer-12,..],[],...]

    package_valid = models.BooleanField(default=True)
    inclusions_updated = models.BooleanField(default=False)
    itinerary_updated = models.BooleanField(default=False)
    package_inclusions = models.BooleanField(default=False)
    package_itinerary = models.BooleanField(default=False)
    package_active = models.BooleanField(default=True)
    validity_start_date = models.DateField(default=datetime.date.today,blank=True,null=True)
    validity_end_date = models.DateField(blank=True,null=True)

    price = models.DecimalField(max_digits=8, decimal_places=2,blank=True,null=True)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse("SalesApp:package_detail",kwargs={'pk':self.pk})


class Quote(models.Model):
    lead = models.ForeignKey(Lead,on_delete=models.PROTECT)
    adults = models.PositiveSmallIntegerField()
    children = models.PositiveSmallIntegerField(blank=True,null=True)
    children_age = models.CharField(max_length=100,blank=True)
    title = models.CharField(max_length=100)
    starting_place = models.CharField(max_length=100)
    destinations = models.ManyToManyField(Destination)
    cities = models.ManyToManyField(City)
    start_date = models.DateField()
    end_date = models.DateField()
    price = models.DecimalField(max_digits=8, decimal_places=2,default=0,blank=True,null=True)
    mark_up = models.DecimalField(max_digits=8, decimal_places=2,default=0)
    discount = models.DecimalField(max_digits=8, decimal_places=2,default=0)
    itinerary = models.TextField(blank=True) # FORMAT-- [[transport-45,transfer-6,sightseeing-31],[sightseeing-56,transfer-12,..],[],...]
    booked = models.BooleanField(default=False)
    quote_valid = models.BooleanField(default=False)
    inclusions_updated = models.BooleanField(default=False)
    itinerary_updated = models.BooleanField(default=False)
    quote_inclusions = models.BooleanField(default=False)
    quote_itinerary = models.BooleanField(default=False)
    quote_active = models.BooleanField(default=True)
    inclusions_format = models.CharField(max_length=100,choices=[('FIXED','Fixed Inlusions'),('CUSTOM','Customized Inclusions'),('FLEXIBLE','Full Flexible Format')], default='CUSTOM')

    def __str__(self):
        return '{} | {}'.format(self.lead, self.title)

    def get_absolute_url(self):
        return reverse("SalesApp:quote_detail",kwargs={'pk':self.pk})

    def get_included_objects(self):
        objects_list = []
        if self.quote_inclusions:
            for inclusion in self.inclusion_set.all():
                if inclusion.item_type == 'TRANSFER':
                    objects_list += list(inclusion.transfers.all())
                elif inclusion.item_type == 'SIGHTSEEING':
                    objects_list += list(inclusion.sightseeings.all())
                elif inclusion.item_type == 'TRANSPORT':
                    objects_list += list(inclusion.transports.all())
                elif inclusion.item_type == 'VARIABLE_TRANSPORT':
                    objects_list.append(inclusion.variable_transports)
                elif inclusion.item_type == 'VISA':
                    objects_list += list(inclusion.visas.all())
                elif inclusion.item_type == 'INSURANCE':
                    objects_list.append(inclusion.insurance)
                else:
                    objects_list.append(inclusion)
        return objects_list

    def get_daywise_itinerary_objects(self):
        itinerary_objects_list = []
        if self.quote_itinerary:
            include_list = json.loads(self.itinerary)
            for day in include_list:
                object_list = []
                for item in day:
                    if item:
                        [object_type,id] = item.split('-')
                        if object_type == 'transfer':
                            object_list.append(Transfer.objects.get(id=id))
                        elif object_type == 'sightseeing':
                            object_list.append(Sightseeing.objects.get(id=id))
                        elif object_type == 'transport':
                            object_list.append(Transport.objects.get(id=id))
                        elif object_type == 'other':
                            object_list.append(Inclusion.objects.get(id=id))
                itinerary_objects_list.append(object_list)
        return itinerary_objects_list

    def get_quote_price_list(self):
        date = self.end_date
        adults = self.adults
        children_age = self.children_age

        auto_price = 0
        objects_price_list = []
        if self.quote_inclusions:
            for inclusion in self.inclusion_set.all():
                if inclusion.item_type in ['FLIGHT','HOTEL','OTHER']:
                    object = inclusion
                    price = inclusion.price if not inclusion.fixed_package_item else None
                    error = False
                    objects_price_list.append([object,price,error])
                    if price and price != 'Pricing Error':
                        auto_price += price
                elif inclusion.item_type == 'VARIABLE_TRANSPORT':
                    object = inclusion.variable_transports
                    price = inclusion.price if not inclusion.fixed_package_item else None
                    error = False
                    objects_price_list.append([object,price,error])
                    if price and price != 'Pricing Error':
                        auto_price += price
                elif inclusion.item_type == 'INSURANCE':
                    object = inclusion.insurance
                    p = Pricing.pricemanager.get_object_pricing(object=object,adults=adults,children_age=children_age,date=date)
                    price = p if not inclusion.fixed_package_item else None
                    error = True if p == 'Pricing Error' else False
                    objects_price_list.append([object,price,error])
                    if price and price != 'Pricing Error':
                        auto_price += price
                elif inclusion.item_type in ['TRANSPORT','TRANSFER','SIGHTSEEING','VISA']:
                    if inclusion.item_type == 'TRANSPORT':
                        objects = inclusion.transports.all()
                    elif inclusion.item_type == 'TRANSFER':
                        objects = inclusion.transfers.all()
                    elif inclusion.item_type == 'SIGHTSEEING':
                        objects = inclusion.sightseeings.all()
                    elif inclusion.item_type == 'VISA':
                            objects = inclusion.visas.all()
                    for object in objects:
                        p = Pricing.pricemanager.get_object_pricing(object=object,adults=adults,children_age=children_age,date=date)
                        price = p if not inclusion.fixed_package_item else None
                        error = True if p == 'Pricing Error' else False
                        objects_price_list.append([object,price,error])
                        if price and price != 'Pricing Error':
                            auto_price += price
                elif inclusion.item_type == 'EXCLUSION':
                    objects_price_list.append([inclusion,0,False])
        self.price = auto_price + self.mark_up - self.discount
        self.save()
        return objects_price_list, auto_price


class Inclusion(models.Model):
    item_type_choices = [('FLIGHT','Flight'),('HOTEL','Hotel'),('TRANSPORT','Fixed Price Transport'),('VARIABLE_TRANSPORT','Variable Price Transport'),
                            ('TRANSFER','Transfer'),('SIGHTSEEING','Sightseeing'),('VISA','Visa'),('INSURANCE','Insurance'),('OTHER','Other'),('EXCLUSION','Exclusion')]
    package = models.ForeignKey(Package,on_delete=models.CASCADE,blank=True,null=True)
    quote = models.ForeignKey(Quote,on_delete=models.CASCADE,blank=True,null=True)
    item_type = models.CharField(max_length=50,choices=item_type_choices)
    other_type = models.CharField(max_length=50,choices=[('TRANSPORT','Transport'),('TRANSFER','Transfer'),('SIGHTSEEING','Sightseeing'),('OTHER','Other')],default='OTHER')
    date = models.DateField(blank=True,null=True)
    checkin_date = models.DateField(blank=True,null=True)
    checkout_date = models.DateField(blank=True,null=True)
    nights = models.PositiveSmallIntegerField(blank=True,null=True)
    no_of_rooms = models.PositiveSmallIntegerField(blank=True,null=True)
    room_type = models.CharField(max_length=100,blank=True)
    airline = models.CharField(max_length=50,blank=True)
    name = models.CharField(max_length=100,blank=True)
    details = models.TextField(max_length=1000,blank=True)
    hotel_group = models.ForeignKey(HotelGroup,on_delete=models.CASCADE,blank=True,null=True)
    transports = models.ManyToManyField(Transport,related_name='Fixed_Inclusions',blank=True)
    variable_transports = models.ForeignKey(Transport,related_name='Variable_Inclusions',on_delete=models.CASCADE,blank=True,null=True)
    hotel = models.ForeignKey(Hotel,on_delete=models.CASCADE,blank=True,null=True)
    transfers = models.ManyToManyField(Transfer,blank=True)
    sightseeings = models.ManyToManyField(Sightseeing,blank=True)
    visas = models.ManyToManyField(Visa,blank=True)
    insurance = models.ForeignKey(Insurance,on_delete=models.CASCADE,blank=True,null=True)
    city = models.ForeignKey(City,on_delete=models.CASCADE,blank=True,null=True)
    price = models.DecimalField(max_digits=8, decimal_places=2,blank=True,null=True)

    fixed_package_item = models.BooleanField(default=False)
    freeze = models.BooleanField(default=False)
    optional = models.BooleanField(default=False)
    include = models.BooleanField(default=False)
    display_order = models.PositiveSmallIntegerField(blank=True,null=True)


class FlexInclusions(models.Model):
    quote = models.OneToOneField(Quote,on_delete=models.CASCADE,blank=True,null=True)
    flights = models.TextField(max_length=1000)
    transport = models.TextField(max_length=1000)
    hotels = models.TextField(max_length=1000)
    transfers = models.TextField(max_length=1000)
    sightseeing = models.TextField(max_length=1000)
    visa = models.TextField(max_length=400)
    insurance = models.TextField(max_length=400)
    others = models.TextField(max_length=1000)
    exclusions = models.TextField(max_length=1000)

    def get_absolute_url(self):
        return reverse("SalesApp:quote_detail",kwargs={'pk':self.quote.pk})

class FlexItinerary(models.Model):
    quote = models.OneToOneField(Quote,on_delete=models.CASCADE,blank=True,null=True)
    content = models.TextField(max_length=1000)

    def get_absolute_url(self):
        return reverse("SalesApp:quote_detail",kwargs={'pk':self.quote.pk})
