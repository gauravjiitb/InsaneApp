import django_filters
from SalesApp.models import Customer,Lead


class CustomerFilter(django_filters.FilterSet):
    class Meta:
        model = Customer
        fields = {
            'name':['icontains'],
        }


class LeadFilter(django_filters.FilterSet):
    customer = django_filters.ModelChoiceFilter(queryset=Customer.objects.all().order_by('name'))
    lead_status = django_filters.ChoiceFilter(choices=Lead.lead_status_choices)
    class Meta:
        model = Lead
        fields = {
            'trip_id':['iexact'],
            'destinations':['icontains'],
            'customer':[],
            'lead_status':[],
        }
