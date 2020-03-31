from django.db import models
from django.urls import reverse
import uuid
# Create your models here.

class Customer(models.Model):
    name = models.CharField(max_length=256)
    email = models.EmailField(unique=True)
    phone = models.PositiveIntegerField()

    def get_absolute_url(self):
        return reverse("SalesApp:customer_detail",kwargs={'pk':self.pk})

    def __str__(self):
        return self.name


class Lead(models.Model):
    lead_source_choices = [
        ('FNF', 'Friends & Family'),
        ('TT', 'Travel Triangle'),
        ('CRF', 'Customer Referral'),
        ('RPC', 'Repeat Customer'),
        ('FBAD','Facebook Ads'),
        ('B2B','B2B'),
        ('WEB','Website / Online Forums'),
    ]
    lead_status_choices = [
        ('NEW', 'New Enquiry'),
        ('QUOTED', 'Quoted'),
        ('BOOKED', 'Booked')
    ]

    customer = models.ForeignKey(Customer,related_name='Leads',on_delete=models.PROTECT)
    destinations = models.CharField(max_length=256)
    lead_source = models.CharField(max_length=256,choices=lead_source_choices,default='FNF')
    lead_source_id = models.CharField(max_length=25,blank=True)
    lead_status = models.CharField(max_length=25,choices=lead_status_choices,default='NEW')
    remarks = models.TextField(blank=True)
    trip_id = models.CharField(max_length=10,editable=False,unique=True)
    creation_date = models.DateField(auto_now=True)

    def save(self, *args, **kwargs):
        self.trip_id = "IN"+uuid.uuid1().hex[:5].upper()
        super().save(*args, **kwargs)

    def __str__(self):
        return self.trip_id

    def get_absolute_url(self):
        return reverse("SalesApp:lead_detail",kwargs={'pk':self.pk})
