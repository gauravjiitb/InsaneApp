from django.contrib import admin

from ContentApp.models import Destination,City,Hotel,Transfer,Sightseeing,Vendor

# Register your models here.

admin.site.register(Destination)
admin.site.register(City)
admin.site.register(Hotel)
admin.site.register(Transfer)
admin.site.register(Sightseeing)
admin.site.register(Vendor)
