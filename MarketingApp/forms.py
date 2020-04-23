from django import forms

from MarketingApp.models import Inquiry


class InquiryForm(forms.ModelForm):
    follow_up_date = forms.DateField(required=False,widget=forms.DateInput(format='%d/%m/%y'),input_formats=('%d/%m/%y', ))
    class Meta:
        model = Inquiry
        exclude = ['owner','assigned_staff']

class InquiryAssignForm(forms.ModelForm):
    class Meta:
        model = Inquiry
        fields = ['owner','assigned_staff']
