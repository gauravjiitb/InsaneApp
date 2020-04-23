import django_filters

from ProfilesApp.models import Customer
from SalesApp.models import Lead
from OperationsApp.models import Booking

class BookingFilter(django_filters.FilterSet):
    lead = django_filters.ModelChoiceFilter(queryset=Lead.objects.all())
    status = django_filters.ChoiceFilter(choices=Booking.status_choices)
    class Meta:
        model = Booking
        fields = {
            'booked_destinations':['icontains'],
            'lead':[],
            'status':[],
        }
    @property
    def qs(self):
        parent = super().qs
        return parent.exclude(status='CLOSED')
