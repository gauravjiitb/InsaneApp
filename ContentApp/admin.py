from django.contrib import admin

from ContentApp.models import Destination,City,Hotel,Transport,Transfer,Sightseeing,Vendor,Visa,Insurance, Pricing

class DestinationAdmin(admin.ModelAdmin):
    list_display = ('id','name')


class VendorAdmin(admin.ModelAdmin):
    list_display = ('id','name')


class CityAdmin(admin.ModelAdmin):
    list_display = ('id','name')

class SightseeingAdmin(admin.ModelAdmin):
    list_display = ('id','name')

# Register your models here.

admin.site.register(Destination,DestinationAdmin)
admin.site.register(City,CityAdmin)
admin.site.register(Transport)
admin.site.register(Hotel)
admin.site.register(Transfer)
admin.site.register(Sightseeing,SightseeingAdmin)
admin.site.register(Vendor,VendorAdmin)
admin.site.register(Visa)
admin.site.register(Insurance)
admin.site.register(Pricing)
