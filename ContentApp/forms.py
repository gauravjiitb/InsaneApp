from django import forms
from django.forms import formset_factory

from ContentApp.models import Transfer


class TransferForm(forms.ModelForm):
    max_pax = forms.IntegerField(min_value=1)
    price = forms.FloatField(min_value=0)
    class Meta:
        model = Transfer
        fields = ['city','name','transfer_type','description','max_pax','price']
