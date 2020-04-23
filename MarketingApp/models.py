from django.db import models
from django.urls import reverse_lazy,reverse

from phonenumber_field.modelfields import PhoneNumberField

from ContentApp.models import Destination
from ProfilesApp.models import Staff


# Create your models here.

class LeadSource(models.Model):
    name = models.CharField(max_length=256,unique=True)

    def __str__(self):
        return self.name
    # lead_source_choices = [
    #     ('FNF', 'Friends & Family'),
    #     ('TT', 'Travel Triangle'),
    #     ('CRF', 'Customer Referral'),
    #     ('RPC', 'Repeat Customer'),
    #     ('FBAD','Facebook Ads'),
    #     ('B2B','B2B'),
    #     ('WEB','Website / Online Forums'),
    # ]

class Inquiry(models.Model):
    inquiry_status_choices = [
        ('NEW', 'New Enquiry'),
        ('ARCHIVED', 'Archived'),
        ('LEAD', 'Lead Created')
    ]
    creation_date = models.DateField(editable=False,auto_now=True)
    name = models.CharField(max_length=256)
    follow_up_date = models.DateField(blank=True,null=True)
    remarks = models.CharField(max_length=256,blank=True)
    email = models.EmailField(blank=True)
    phone = PhoneNumberField(blank=True)
    description = models.CharField(max_length=256,blank=True)
    places = models.ManyToManyField(Destination,related_name='Inquiries',blank=True)
    source = models.ForeignKey(LeadSource,related_name='Inquiries',blank=True,null=True,on_delete=models.PROTECT)
    id_at_source = models.CharField(max_length=30,blank=True)
    status = models.CharField(max_length=25,choices=inquiry_status_choices,default='NEW')
    owner = models.ForeignKey(Staff,related_name='Inquiries',on_delete=models.PROTECT,blank=True,null=True)
    assigned_staff = models.ManyToManyField(Staff,related_name='AssignedInquiries',blank=True)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("MarketingApp:inquiry_list")
