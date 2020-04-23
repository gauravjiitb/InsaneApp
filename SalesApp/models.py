from django.db import models
from django.urls import reverse

from MarketingApp.models import LeadSource
from ProfilesApp.models import Customer,Staff
from ContentApp.models import Destination

#########################################
# HELPER FUNCTIONS

def get_trip_id():
    # try:
    last_lead = Lead.objects.all().order_by('id').last()
    new_trip_id = "IN"+ str(170002+last_lead.id)
    return new_trip_id
    # except:
    #     return 'IN170001'


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
