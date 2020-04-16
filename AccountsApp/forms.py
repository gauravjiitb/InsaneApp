from django import forms
from django.forms import formset_factory,modelformset_factory

from AccountsApp.models import Account,TransactionHead,Transaction,TripPayment,PendingPayment,TripPaymentHead
from ContentApp.models import Vendor


class TransactionForm(forms.ModelForm):
    date = forms.DateField(widget=forms.DateInput(format='%d/%m/%y'),input_formats=('%d/%m/%y', ))
    class Meta:
        model = Transaction
        fields = ('date','account','transaction_ref','amount','description','inout_type','balance','transaction_head','remarks','reference_number','reconcile_details')

class TransactionUploadForm(forms.Form):
    date = forms.DateField(widget=forms.DateInput(format='%d/%m/%y'),input_formats=('%d/%m/%y', ))
    amount = forms.DecimalField(max_digits=19,decimal_places=2)
    reference = forms.CharField(max_length=256)
    debitamount = forms.DecimalField(max_digits=19,decimal_places=2)
    creditamount = forms.DecimalField(max_digits=19,decimal_places=2)
    balance = forms.DecimalField(max_digits=19,decimal_places=2)
    description = forms.CharField(max_length=500)
    reference_num = forms.CharField(max_length=256)
    reconcile_details = forms.CharField(max_length=256)
    transaction_head = forms.ModelChoiceField(queryset=TransactionHead.objects.all())
    remarks = forms.CharField(max_length=256,required=False)
    reconcile_bool = forms.BooleanField(initial=False,required=False)
    inout_type = forms.ChoiceField(choices=[('DR','Debit'),('CR','Credit')],widget=forms.Select())
    fields = ('date','amount','reference','debitamount','creditamount','balance','description','reference_num','reconcile_details','transaction_head','remarks','reconcile_bool','inout_type')
    def __init__(self, *args, **kwargs):
        super(TransactionUploadForm, self).__init__(*args, **kwargs)
        self.empty_permitted = True
    def __str__(self):
        return self.description

TransactionUploadFormSet = formset_factory(TransactionUploadForm,extra=0)

class PendingPaymentForm(forms.ModelForm):
    date = forms.DateField(widget=forms.DateInput(format='%d/%m/%y'),input_formats=('%d/%m/%y', ))
    class Meta:
        model = PendingPayment
        fields = ('date','amount',)
    def __init__(self, *args, **kwargs):
        super(PendingPaymentForm, self).__init__(*args, **kwargs)
        self.empty_permitted = True

PendingPaymentFormSet = formset_factory(PendingPaymentForm,extra=2)

class TripPaymentForm(forms.ModelForm):
    vendor = forms.ModelChoiceField(queryset=Vendor.objects.all(),required=False)
    date = forms.DateField(widget=forms.DateInput(format='%d/%m/%y'),input_formats=('%d/%m/%y', ))
    transaction = forms.ModelChoiceField(queryset=Transaction.objects.all(),required=False)
    date = forms.DateField(widget=forms.DateInput(format='%d/%m/%y'),input_formats=('%d/%m/%y', ),required=False)
    class Meta:
        model = TripPayment
        fields = ('date','transaction','amount','inout_type','booking','description','vendor')
    def __init__(self, *args, **kwargs):
        super(TripPaymentForm, self).__init__(*args, **kwargs)
        self.empty_permitted = True

TripPaymentFormSet = formset_factory(TripPaymentForm,extra=0)
