from django.contrib import admin
from SalesApp.models import Lead,Quote,Package,Inclusion, FlexInclusions,FlexItinerary, HotelGroup

# Create your custom admin views here.

class LeadAdmin(admin.ModelAdmin):
    list_display = ('id','creation_date','trip_id','customer','lead_status')

class QuoteAdmin(admin.ModelAdmin):
    list_display = ('id','lead')

# Register your models here.

admin.site.register(Lead,LeadAdmin)
admin.site.register(Quote,QuoteAdmin)
admin.site.register(Package)
admin.site.register(Inclusion)
admin.site.register(HotelGroup)
admin.site.register(FlexInclusions)
admin.site.register(FlexItinerary)
