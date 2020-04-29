from django.contrib import admin

from ContentApp.models import Destination,City,Hotel,Transfer,Sightseeing,Vendor,Visa,Insurance

class DestinationAdmin(admin.ModelAdmin):
    list_display = ('id','name')


class VendorAdmin(admin.ModelAdmin):
    list_display = ('id','name')


class CityAdmin(admin.ModelAdmin):
    list_display = ('id','name')


# Register your models here.

admin.site.register(Destination,DestinationAdmin)
admin.site.register(City,CityAdmin)
admin.site.register(Hotel)
admin.site.register(Transfer)
admin.site.register(Sightseeing)
admin.site.register(Vendor,VendorAdmin)
admin.site.register(Visa)
admin.site.register(Insurance)
