from django.contrib import admin

from MarketingApp.models import LeadSource,Inquiry


class LeadSourceAdmin(admin.ModelAdmin):
    list_display = ('id','name')

# Register your models here.


admin.site.register(LeadSource,LeadSourceAdmin)
admin.site.register(Inquiry)
