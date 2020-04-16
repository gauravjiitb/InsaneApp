import django_filters
from django.db import models
from django import forms

from AccountsApp.models import Account,TransactionHead,Transaction,TripPayment,PendingPayment
from OperationsApp.models import Booking

class TransactionFilter(django_filters.FilterSet):
    # account = django_filters.ModelChoiceFilter(queryset=Account.objects.all())
    transaction_head = django_filters.ModelChoiceFilter(queryset=TransactionHead.objects.all())
    # inout_type = django_filters.ChoiceFilter(choices=[('DR','Debit'),('CR','Credit')])
    date_lt = django_filters.DateFilter(field_name='date', lookup_expr='lt',widget=forms.DateInput(format='%d/%m/%y'),input_formats=('%d/%m/%y', ))
    date_gt = django_filters.DateFilter(field_name='date', lookup_expr='gt',widget=forms.DateInput(format='%d/%m/%y'),input_formats=('%d/%m/%y', ))
    class Meta:
        model = Transaction
        fields = {
            # 'account':[],
            # 'inout_type':[],
            'transaction_head':[],
        }


class TripPaymentFilter(django_filters.FilterSet):
    booking = django_filters.ModelChoiceFilter(queryset=Booking.objects.all().order_by('trip_id'))
    date_lt = django_filters.DateFilter(field_name='date', lookup_expr='lt',widget=forms.DateInput(format='%d/%m/%y'),input_formats=('%d/%m/%y', ))
    date_gt = django_filters.DateFilter(field_name='date', lookup_expr='gt',widget=forms.DateInput(format='%d/%m/%y'),input_formats=('%d/%m/%y', ))
    class Meta:
        model = TripPayment
        fields = {
            'booking':[],
        }
    # @property
    # def qs(self):
    #     parent = super().qs
    #     return parent.filter(vendor__isnull=True)
