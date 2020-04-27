from django.contrib import admin
from SalesApp.models import Lead,Quote,QuoteHotelInfo, QuoteTransferInfo

# Create your custom admin views here.

class LeadAdmin(admin.ModelAdmin):
    list_display = ('id','creation_date','trip_id','customer','lead_status')

class QuoteAdmin(admin.ModelAdmin):
    list_display = ('id','lead')

# Register your models here.

admin.site.register(Lead,LeadAdmin)
admin.site.register(Quote,QuoteAdmin)
admin.site.register(QuoteHotelInfo)
admin.site.register(QuoteTransferInfo)
