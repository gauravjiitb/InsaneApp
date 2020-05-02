from django.contrib import admin
from SalesApp.models import (Lead,Quote,QuoteHotelInfo, QuoteTransferInfo,QuoteSightseeingInfo,QuoteVisaInfo,
                                QuoteInsuranceInfo,QuoteItineraryInfo,FlexInclusions,FlexItinerary,QuoteFlightInfo,QuoteTransportInfo,
                                QuoteOthersInfo)

# Create your custom admin views here.

class LeadAdmin(admin.ModelAdmin):
    list_display = ('id','creation_date','trip_id','customer','lead_status')

class QuoteAdmin(admin.ModelAdmin):
    list_display = ('id','lead')

# Register your models here.

admin.site.register(Lead,LeadAdmin)
admin.site.register(Quote,QuoteAdmin)
admin.site.register(QuoteFlightInfo)
admin.site.register(QuoteTransportInfo)
admin.site.register(QuoteHotelInfo)
admin.site.register(QuoteTransferInfo)
admin.site.register(QuoteSightseeingInfo)
admin.site.register(QuoteVisaInfo)
admin.site.register(QuoteInsuranceInfo)
admin.site.register(QuoteItineraryInfo)
admin.site.register(FlexInclusions)
admin.site.register(FlexItinerary)
