from django.db import models
from django.urls import reverse
from django.utils.encoding import smart_str

from SalesApp.models import Customer,Lead

# Create your models here.

class Booking(models.Model):
    status_choices = [
        ('BOOKED', 'Booked'),
        ('TRAVELLED', 'Travelled'),
        ('CLOSED', 'Closed')
    ]

    lead = models.OneToOneField(Lead,related_name='Booking',on_delete=models.PROTECT)
    customer = models.ForeignKey(Customer,related_name='Booking',editable=False,on_delete=models.PROTECT,null=True)
    status = models.CharField(max_length=25,choices=status_choices,default='BOOKED')
    booking_date = models.DateField()
    travel_date = models.DateField()
    booked_destinations = models.CharField(max_length=256)
    sale_amount = models.DecimalField(max_digits=19,decimal_places=2,blank=True,null=True)
    projected_revenue = models.DecimalField(max_digits=19,decimal_places=2,blank=True,null=True)
    actual_revenue = models.DecimalField(max_digits=19,decimal_places=2,blank=True,null=True)
    tcs_amount = models.DecimalField(max_digits=19,decimal_places=2,blank=True,null=True)
    gst_amount = models.DecimalField(max_digits=19,decimal_places=2,blank=True,null=True)
    commission_paid = models.DecimalField(max_digits=19,decimal_places=2,blank=True,null=True)
    trip_id = models.CharField(max_length=10,editable=False)

    def save(self, *args, **kwargs):
        self.trip_id = self.lead.trip_id
        self.customer = self.lead.customer
        super().save(*args, **kwargs)

    def __str__(self):
        booking_display_name =  '{} - {}'.format(self.lead.trip_id, self.lead.customer.name)
        return booking_display_name

    def get_absolute_url(self):
        return reverse("OperationsApp:booking_detail",kwargs={'pk':self.pk})
