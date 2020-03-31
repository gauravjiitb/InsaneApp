from django import forms

from OperationsApp.models import Booking

class BookingForm(forms.ModelForm):
    class Meta:
        model = Booking
        fields = ('lead','status','booking_date','travel_date','booked_destinations','sale_amount',
                    'projected_revenue','actual_revenue','tcs_amount','gst_amount','commission_paid')
