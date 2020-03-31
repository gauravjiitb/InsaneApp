from django.contrib import admin

from SalesApp.models import Customer,Lead
from OperationsApp.models import Booking

# Create your custom admin views here.

class BookingAdmin(admin.ModelAdmin):
    list_display = ('id','lead','status','booked_destinations','sale_amount')

# Register your models here.

admin.site.register(Booking,BookingAdmin)
