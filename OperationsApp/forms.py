from django import forms

from django.forms import modelformset_factory

from OperationsApp.models import Booking, BookingItem
from SalesApp.models import Quote
from ProfilesApp.models import Traveler
from ProfilesApp.forms import TravelerForm

class BookingForm(forms.ModelForm):
    quote = forms.ModelChoiceField(queryset=Quote.objects.all(),disabled=True)
    booking_date = forms.DateField(widget=forms.DateInput(format='%d/%m/%y'),input_formats=('%d/%m/%y', ))
    class Meta:
        model = Booking
        fields = ('quote','status','booking_date','travelers','sale_amount','projected_revenue','actual_revenue','tcs_amount','gst_amount','commission_paid')
    def save(self, commit=True):
        if commit:
            f = super(BookingForm, self).save(commit=True)
            quote = f.quote
            quote.booked = True
            quote.save()
            lead = f.quote.lead
            lead.lead_status = 'BOOKED'
            lead.save()
        else:
            f = super(BookingForm, self).save(commit=False)
        return f

class BookingItemForm(forms.ModelForm):
    date = forms.DateField(widget=forms.DateInput(format='%d/%m/%y'),input_formats=('%d/%m/%y', ),required=False)
    time_limit = forms.DateField(widget=forms.DateInput(format='%d/%m/%y'),input_formats=('%d/%m/%y', ),required=False)
    class Meta:
        model = BookingItem
        fields = ('date','display_handle','vendor','cost','time_limit','conf_status')

AddTravelersFS = modelformset_factory(Traveler,form=TravelerForm,extra=3,can_delete=True)
