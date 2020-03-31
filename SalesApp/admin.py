from django.contrib import admin
from SalesApp.models import Customer,Lead

# Create your custom admin views here.

class LeadAdmin(admin.ModelAdmin):
    list_display = ('id','creation_date','trip_id','customer','lead_status','destinations')

class CustomerAdmin(admin.ModelAdmin):
    list_display = ('name','email','phone')
    # list_select_related = ('Lead',)

# Register your models here.

admin.site.register(Customer,CustomerAdmin)
admin.site.register(Lead,LeadAdmin)
