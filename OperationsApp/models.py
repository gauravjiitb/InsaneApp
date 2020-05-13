from django.db import models
from django.urls import reverse
from django.utils.encoding import smart_str

from SalesApp.models import Lead, Quote
from ProfilesApp.models import Customer,Staff
from ContentApp.models import Destination, Vendor


# Create your models here.

class Booking(models.Model):
    status_choices = [
        ('BOOKED', 'Booked'),
        ('TRAVELLED', 'Travelled'),
        ('CLOSED', 'Closed')
    ]
    # lead = models.OneToOneField(Lead,related_name='Booking',on_delete=models.PROTECT)
    quote = models.OneToOneField(Quote,related_name='Booking',on_delete=models.PROTECT,blank=True,null=True)
    status = models.CharField(max_length=25,choices=status_choices,default='BOOKED')
    booking_date = models.DateField()
    itinerary = models.TextField(blank=True)
    # travel_date = models.DateField(blank=True,null=True)
    # booked_destinations = models.ManyToManyField(Destination,related_name='Bookings',blank=True,null=True)
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
    item_type_choices = [('FLIGHT','Flights'),('HOTEL','Hotels'),('TRANSPORT','Transport'),('TRANSFER','Transfer'),
                            ('SIGHTSEEING','Sightseeing'),('VISA','Visa'),('INSURANCE','Insurance'),('OTHER','Others'),('EXCLUSION','Exclusions')]
    booking = models.ForeignKey(Booking,on_delete=models.CASCADE,blank=True,null=True)
    item_type = models.CharField(max_length=50,choices=item_type_choices)
    date = models.DateField(blank=True,null=True)
    detail = models.TextField(blank=True,null=True)
    vendor = models.ForeignKey(Vendor,on_delete=models.PROTECT,blank=True,null=True)
    cost = models.DecimalField(max_digits=10, decimal_places=2,blank=True,null=True)
    time_limit = models.DateField(blank=True,null=True)
    conf_status = models.CharField(max_length=50,choices=[('PENDING','Pending'),('BLOCKED','Blocked'),('CONFIRMED','Confirmed')],default='PENDING')
    display_order = models.PositiveSmallIntegerField(blank=True,null=True)

class Traveler(models.Model):
    firstname = models.CharField(max_length=100,blank=True,null=True)
    lastname = models.CharField(max_length=100,blank=True,null=True)
    gender = models.CharField(max_length=50,choices=[('MALE','Male'),('FEMALE','Female')])
    dob = models.DateField(blank=True,null=True)
    passport_num = models.CharField(max_length=50,blank=True,null=True)
    place_of_issue = models.CharField(max_length=50,blank=True,null=True)
    expiry_date = models.DateField(blank=True,null=True)
    issue_Date = models.DateField(blank=True,null=True)

    def __str__(self):
        return '{} {}'.format(self.firstname, self.lastname)
