from django.db import models
from django.urls import reverse
from django.utils.encoding import smart_str

from SalesApp.models import Lead, Quote, Inclusion
from ProfilesApp.models import Staff, Traveler
from ContentApp.models import Destination, Vendor


# Create your models here.

class Booking(models.Model):
    status_choices = [
        ('BOOKED', 'Booked'),
        ('TRAVELLED', 'Travelled'),
        ('CLOSED', 'Closed')
    ]
    quote = models.OneToOneField(Quote,related_name='Booking',on_delete=models.PROTECT,blank=True,null=True)
    status = models.CharField(max_length=25,choices=status_choices,default='BOOKED')
    booking_date = models.DateField()
    itinerary = models.TextField(blank=True)
    travelers = models.ManyToManyField(Traveler)
    sale_amount = models.DecimalField(max_digits=10,decimal_places=2,blank=True,null=True)
    projected_revenue = models.DecimalField(max_digits=10,decimal_places=2,blank=True,null=True)
    actual_revenue = models.DecimalField(max_digits=10,decimal_places=2,blank=True,null=True)
    tcs_amount = models.DecimalField(max_digits=10,decimal_places=2,blank=True,null=True)
    gst_amount = models.DecimalField(max_digits=10,decimal_places=2,blank=True,null=True)
    commission_paid = models.DecimalField(max_digits=10,decimal_places=2,blank=True,null=True)
    owner = models.ForeignKey(Staff,related_name='Bookings',on_delete=models.PROTECT,blank=True,null=True)
    assigned_staff = models.ManyToManyField(Staff,related_name='AssignedBookings',blank=True)

    def __str__(self):
        booking_display_name =  '{} - {}'.format(self.quote.lead.trip_id, self.quote.lead.customer.user.name)
        return booking_display_name

    def get_absolute_url(self):
        return reverse("OperationsApp:booking_detail",kwargs={'pk':self.pk})

class BookingItem(models.Model):
    item_type_choices = [('0_FLIGHT','Flight'),('1_HOTEL','Hotel'),('2_TRANSPORT','Transport'),('3_TRANSFER','Transfer'),('4_SIGHTSEEING','Sightseeing'),
                            ('5_VISA','Visa'),('6_INSURANCE','Insurance'),('7_OTHER','Other'),('8_EXCLUSION','Exclusion')]
    booking = models.ForeignKey(Booking,on_delete=models.CASCADE,blank=True,null=True)
    item_type = models.CharField(max_length=50,choices=item_type_choices)
    inclusion = models.ForeignKey(Inclusion,on_delete=models.SET_NULL,blank=True,null=True)
    date = models.DateField(blank=True,null=True)
    display_handle = models.TextField(blank=True,null=True)
    vendor = models.ForeignKey(Vendor,on_delete=models.PROTECT,blank=True,null=True)
    cost = models.DecimalField(max_digits=10, decimal_places=2,blank=True,null=True)
    time_limit = models.DateField(blank=True,null=True)
    conf_status = models.CharField(max_length=50,choices=[('PENDING','Pending'),('BLOCKED','Blocked'),('CONFIRMED','Confirmed')],default='PENDING')
