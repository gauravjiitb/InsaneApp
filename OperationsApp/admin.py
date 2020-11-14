from django.contrib import admin

from SalesApp.models import Customer,Lead
from OperationsApp.models import Booking, BookingItem

# Create your custom admin views here.

class BookingAdmin(admin.ModelAdmin):
    list_display = ('id','quote','status','sale_amount')

# Register your models here.

admin.site.register(Booking,BookingAdmin)
admin.site.register(BookingItem)
