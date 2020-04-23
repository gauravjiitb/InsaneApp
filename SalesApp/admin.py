from django.contrib import admin
from SalesApp.models import Lead

# Create your custom admin views here.

class LeadAdmin(admin.ModelAdmin):
    list_display = ('id','creation_date','trip_id','customer','lead_status')

# Register your models here.

admin.site.register(Lead,LeadAdmin)
