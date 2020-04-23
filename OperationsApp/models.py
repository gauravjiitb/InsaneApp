from django.db import models
from django.urls import reverse
from django.utils.encoding import smart_str

from SalesApp.models import Lead
from ProfilesApp.models import Customer,Staff
from ContentApp.models import Destination


# Create your models here.

class Booking(models.Model):
    status_choices = [
        ('BOOKED', 'Booked'),
        ('TRAVELLED', 'Travelled'),
        ('CLOSED', 'Closed')
    ]
    lead = models.OneToOneField(Lead,related_name='Booking',on_delete=models.PROTECT)
    status = models.CharField(max_length=25,choices=status_choices,default='BOOKED')
    booking_date = models.DateField()
    travel_date = models.DateField()
    booked_destinations = models.ManyToManyField(Destination,related_name='Bookings')
    sale_amount = models.DecimalField(max_digits=19,decimal_places=2,blank=True,null=True)
    projected_revenue = models.DecimalField(max_digits=19,decimal_places=2,blank=True,null=True)
    actual_revenue = models.DecimalField(max_digits=19,decimal_places=2,blank=True,null=True)
    tcs_amount = models.DecimalField(max_digits=19,decimal_places=2,blank=True,null=True)
    gst_amount = models.DecimalField(max_digits=19,decimal_places=2,blank=True,null=True)
    commission_paid = models.DecimalField(max_digits=19,decimal_places=2,blank=True,null=True)
    owner = models.ForeignKey(Staff,related_name='Bookings',on_delete=models.PROTECT,blank=True,null=True)
    assigned_staff = models.ManyToManyField(Staff,related_name='AssignedBookings',blank=True)

    def __str__(self):
        booking_display_name =  '{} - {}'.format(self.lead.trip_id, self.lead.customer.user.name)
        return booking_display_name

    def get_absolute_url(self):
        return reverse("OperationsApp:booking_detail",kwargs={'pk':self.pk})
