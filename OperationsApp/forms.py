from django import forms

from OperationsApp.models import Booking, BookingItem, Traveler
from SalesApp.models import Quote

class BookingForm(forms.ModelForm):
    quote = forms.ModelChoiceField(queryset=Quote.objects.all(),disabled=True)
    booking_date = forms.DateField(widget=forms.DateInput(format='%d/%m/%y'),input_formats=('%d/%m/%y', ))
    class Meta:
        model = Booking
        fields = ('quote','status','booking_date','sale_amount','projected_revenue','actual_revenue','tcs_amount','gst_amount','commission_paid')
    def save(self, commit=True):
        if commit:
            f = super(BookingForm, self).save(commit=True)
            quote = f.quote
            quote.booked = True
            quote.save()
        else:
            f = super(BookingForm, self).save(commit=False)
        return f

class BookingItemForm(forms.ModelForm):
    date = forms.DateField(widget=forms.DateInput(format='%d/%m/%y'),input_formats=('%d/%m/%y', ),required=False)
    time_limit = forms.DateField(widget=forms.DateInput(format='%d/%m/%y'),input_formats=('%d/%m/%y', ),required=False)
    class Meta:
        model = BookingItem
        fields = ('date','detail','vendor','cost','time_limit','conf_status')
    def save(self, commit=True):
        f = super(BookingItemForm, self).save()
        if commit:
            item_type = f.item_type
            if item_type == 'FLIGHT':
                f.display_order = 1
            elif item_type == 'HOTEL':
                f.display_order = 2
            elif item_type == 'TRANSPORT':
                f.display_order = 3
            elif item_type == 'TRANSFER':
                f.display_order = 5
            elif item_type == 'SIGHTSEEING':
                f.display_order = 6
            elif item_type == 'VISA':
                f.display_order = 7
            elif item_type == 'INSURANCE':
                f.display_order = 8
            elif item_type == 'OTHER':
                f.display_order = 9
            elif item_type == 'EXCLUSION':
                f.display_order = 10
            f.save()
        return f



class TravelerForm(forms.ModelForm):
    dob = forms.DateField(widget=forms.DateInput(format='%d/%m/%y'),input_formats=('%d/%m/%y', ),required=False)
    expiry_date = forms.DateField(widget=forms.DateInput(format='%d/%m/%y'),input_formats=('%d/%m/%y', ),required=False)
    issue_Date_date = forms.DateField(widget=forms.DateInput(format='%d/%m/%y'),input_formats=('%d/%m/%y', ),required=False)
    class Meta:
        model = Traveler
        fields = ('firstname','lastname','gender','dob','passport_num','place_of_issue','expiry_date','issue_Date')
