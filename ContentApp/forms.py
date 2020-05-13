import datetime

from django import forms
from django.forms import inlineformset_factory

from ContentApp.models import Transfer, Pricing
from SalesApp.models import Package, Quote, Inclusion


###############################################################################
# UTILITY FUNCTIONS
###############################################################################
def int_str_to_list(int_string):
    """ Takes a list of positive integers and returns a list. If improper format, returns empty list"""
    try:
        int_list = list(int_string.split(","))
        for i in range(len(int_list)):
            int_list[i] = int(int_list[i])
            if int_list[i] < 0:
                return []
    except:
        int_list = []
    return int_list


def float_str_to_list(float_string):
    """ Takes a list of positive integers and returns a list. If improper format, returns empty list"""
    try:
        float_list = list(float_string.split(","))
        for i in range(len(float_list)):
            float_list[i] = float(float_list[i])
            if float_list[i] < 0:
                return []
    except:
        float_list = []
    return float_list

###############################################################################

class TransferForm(forms.ModelForm):
    class Meta:
        model = Transfer
        fields = ['name','city','name','transfer_type','description']

class PricingForm(forms.ModelForm):
    valid_from_date = forms.DateField(widget=forms.DateInput(format='%d/%m/%y'),input_formats=('%d/%m/%y', ), initial = datetime.date.today())
    valid_till_date = forms.DateField(widget=forms.DateInput(format='%d/%m/%y'),input_formats=('%d/%m/%y', ), initial = datetime.date.today() + datetime.timedelta(days=365))
    class Meta:
        model = Pricing
        exclude = ('valid',)
    def clean(self):
        cleaned_data = super().clean()
        pricing_type = cleaned_data.get("pricing_type")
        name = cleaned_data.get("name")
        valid_from_date = cleaned_data.get("valid_from_date")
        valid_till_date = cleaned_data.get("valid_till_date")
        adult_cutoff_age = cleaned_data.get("adult_cutoff_age")
        child_cutoff_age = cleaned_data.get("child_cutoff_age")
        flat_adult_price = cleaned_data.get("flat_adult_price")
        flat_child_price = cleaned_data.get("flat_child_price")
        paxwise_max_pax_list = cleaned_data.get("paxwise_max_pax_list")
        paxwise_price_list = cleaned_data.get("paxwise_price_list")

        if pricing_type == 'FLAT':
            if not flat_adult_price:
                self.add_error('flat_adult_price',"Please enter the adult pricing.")
            if not flat_child_price:
                self.add_error('flat_child_price',"Please enter the child pricing.")

        if pricing_type == 'PAXWISE':
            max_pax_list = int_str_to_list(paxwise_max_pax_list)
            price_list = int_str_to_list(paxwise_price_list)
            if (paxwise_max_pax_list and not paxwise_price_list) or (paxwise_price_list and not paxwise_max_pax_list):
                self.add_error('paxwise_max_pax_list',"Paxwise price specified wrongly.")
            if paxwise_max_pax_list and paxwise_price_list and (max_pax_list == [] or paxwise_price_list == [] or len(max_pax_list) != len(price_list)):
                raise forms.ValidationError("Paxwise price specified wrongly.")

PackagePricingFS = inlineformset_factory(Package,Pricing,form=PricingForm,extra=1,can_delete=True)
InclusionPricingFS = inlineformset_factory(Inclusion,Pricing,form=PricingForm,extra=1,can_delete=True)
