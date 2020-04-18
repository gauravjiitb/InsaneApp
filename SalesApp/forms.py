from django import forms

from bootstrap_modal_forms.forms import BSModalForm

from SalesApp.models import Customer,Lead


class CustomerForm(BSModalForm):
    class Meta:
        model = Customer
        fields = ('name','email','phone')

class LeadForm(forms.ModelForm):
    class Meta:
        model = Lead
        fields = ('customer','destinations','lead_source','lead_source_id','lead_status','remarks')

class LeadFromCustomerForm(forms.ModelForm):
    class Meta:
        model = Lead
        fields = ('destinations','lead_source','lead_source_id','lead_status','remarks')
