import django_filters
from MarketingApp.models import LeadSource,Inquiry


class InquiryFilter(django_filters.FilterSet):
    source = django_filters.ModelChoiceFilter(queryset=LeadSource.objects.all())
    class Meta:
        model = Inquiry
        fields = {
            'name':['icontains'],
            'source':[],
            }
