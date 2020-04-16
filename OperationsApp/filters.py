import django_filters
from SalesApp.models import Customer,Lead
from OperationsApp.models import Booking

class BookingFilter(django_filters.FilterSet):
    customer = django_filters.ModelChoiceFilter(queryset=Customer.objects.all().order_by('name'))
    status = django_filters.ChoiceFilter(choices=Booking.status_choices)
    class Meta:
        model = Booking
        fields = {
            'trip_id':['iexact'],
            'booked_destinations':['icontains'],
            'customer':[],
            'status':[],
        }
    @property
    def qs(self):
        parent = super().qs
        return parent.exclude(status='CLOSED')
