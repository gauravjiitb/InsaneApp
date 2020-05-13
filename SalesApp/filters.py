import django_filters
from ProfilesApp.models import Customer
from SalesApp.models import Lead, Package, Quote


class LeadFilter(django_filters.FilterSet):
    customer = django_filters.ModelChoiceFilter(queryset=Customer.objects.all())
    lead_status = django_filters.ChoiceFilter(choices=Lead.lead_status_choices)
    class Meta:
        model = Lead
        fields = {
            'trip_id':['iexact'],
            'destinations':['icontains'],
            'customer':[],
            'lead_status':[],
        }

class PackageFilter(django_filters.FilterSet):
    class Meta:
        model = Package
        fields = {
            'title':['icontains'],
            'type':[],
            }

class QuoteFilter(django_filters.FilterSet):
    class Meta:
        model = Quote
        fields = {
            'title':['icontains'],
            }
