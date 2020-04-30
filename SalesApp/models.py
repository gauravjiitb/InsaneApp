from django.db import models
from django.db.models import Model
from django.urls import reverse

from django_mysql.models import ListCharField

from MarketingApp.models import LeadSource
from ProfilesApp.models import Customer,Staff
from ContentApp.models import Destination,City,Hotel,Transfer,Sightseeing,Visa,Insurance

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


class Quote(models.Model):
    lead = models.ForeignKey(Lead,on_delete=models.PROTECT)
    adults = models.PositiveSmallIntegerField()
    children = models.PositiveSmallIntegerField(blank=True,null=True)
    children_age = models.CharField(max_length=20,blank=True,null=True)
    title = models.CharField(max_length=100)
    starting_place = models.CharField(max_length=100)
    destinations = models.ManyToManyField(Destination)
    cities = models.ManyToManyField(City)
    start_date = models.DateField()
    end_date = models.DateField()

    @property
    def children_age_list(age_string):
        age_list = list(age_string.split(","))
        for i in range(len(age_list)):
            age_list[i] = int(age_list[i])
        return age_list

class QuoteFlightInfo(models.Model):
    quote = models.ForeignKey(Quote,on_delete=models.CASCADE,blank=True,null=True)
    airline = models.CharField(max_length=255,blank=True)
    details = models.TextField(max_length=1000)
    remarks = models.CharField(max_length=255,blank=True)
    price = models.FloatField()

class QuoteTransportInfo(models.Model):
    quote = models.ForeignKey(Quote,on_delete=models.CASCADE,blank=True,null=True)
    type = models.CharField(max_length=100,choices=[('TRAIN','Train'),('BUS','Bus'),('FERRY','Ferry'),('TAXI','Taxi')] )
    date = models.DateField()
    details = models.CharField(max_length=255)
    price = models.FloatField()

class QuoteHotelInfo(models.Model):
    quote = models.ForeignKey(Quote,on_delete=models.CASCADE,blank=True,null=True)
    city = models.ForeignKey(City,on_delete=models.PROTECT)
    hotel = models.ForeignKey(Hotel,on_delete=models.PROTECT)
    checkin_date = models.DateField()
    checkout_date = models.DateField()
    room_type = models.CharField(max_length=100,blank=True)
    no_of_rooms = models.PositiveSmallIntegerField()
    price = models.FloatField()

class QuoteTransferInfo(models.Model):
    quote = models.ForeignKey(Quote,on_delete=models.CASCADE,blank=True,null=True)
    city = models.ForeignKey(City,on_delete=models.PROTECT)
    transfer = models.ForeignKey(Transfer,on_delete=models.PROTECT)
    date = models.DateField()
    quantity = models.PositiveSmallIntegerField()

class QuoteSightseeingInfo(models.Model):
    quote = models.ForeignKey(Quote,on_delete=models.CASCADE,blank=True,null=True)
    city = models.ForeignKey(City,on_delete=models.PROTECT)
    sightseeing = models.ForeignKey(Sightseeing,on_delete=models.PROTECT)
    date = models.DateField()

class QuoteVisaInfo(models.Model):
    quote = models.ForeignKey(Quote,on_delete=models.CASCADE,blank=True,null=True)
    visa = models.ForeignKey(Visa,on_delete=models.PROTECT)

class QuoteInsuranceInfo(models.Model):
    quote = models.ForeignKey(Quote,on_delete=models.CASCADE,blank=True,null=True)
    insurance = models.ForeignKey(Insurance,on_delete=models.PROTECT,blank=True,null=True)

class QuoteItineraryInfo(models.Model):
    quote = models.ForeignKey(Quote,on_delete=models.CASCADE,blank=True,null=True)
    date = models.DateField()
    ordering = models.CharField(max_length=255,blank=True)
    description = models.TextField(blank=True)

class QuoteOthersInfo(models.Model):
    quote = models.ForeignKey(Quote,on_delete=models.CASCADE,blank=True,null=True)
    name = models.CharField(max_length=255)
    description = models.TextField(max_length=1000,blank=True)
    date = models.DateField(blank=True,null=True)
    price = models.FloatField(blank=True,null=True)
