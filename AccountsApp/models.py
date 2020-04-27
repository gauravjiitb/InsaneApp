from django.db import models
from django.urls import reverse
from datetime import date

from SalesApp.models import Customer,Lead
from OperationsApp.models import Booking
from ContentApp.models import Vendor

# Create your models here.

class Account(models.Model):
    name = models.CharField(max_length=255,unique=True)
    detail = models.TextField(blank=True)
    def __str__(self):
        return self.name

class TransactionHead(models.Model):
    name = models.CharField(max_length=255,unique=True)
    trip_bool = models.BooleanField()
    def __str__(self):
        return self.name

class TripPaymentHead(models.Model):
    name = models.CharField(max_length=255,unique=True)
    type = models.CharField(max_length=25,choices=[('CUSTOMER','Customer'),('VENDOR','Vendor')],default='VENDOR')
    def __str__(self):
        return self.name

class Transaction(models.Model):
    date = models.DateField()
    account = models.ForeignKey(Account,related_name='Transactions',on_delete=models.PROTECT)
    transaction_ref = models.CharField(max_length=256)
    amount = models.DecimalField(max_digits=19,decimal_places=2)
    reference_number = models.CharField(max_length=256, blank=True)
    description = models.TextField()
    inout_type = models.CharField(max_length=25,choices=[('DR','Debit'),('CR','Credit')])
    balance = models.DecimalField(max_digits=19,decimal_places=2)
    transaction_head = models.ForeignKey(TransactionHead,related_name='Transactions',on_delete=models.PROTECT)
    remarks = models.CharField(max_length=256,blank=True)
    reconcile_details = models.CharField(max_length=500,blank=True)
    reconcile_status_bool = models.BooleanField(editable=False,default=False)

    def get_absolute_url(self):
        return reverse("AccountsApp:transaction_detail",kwargs={'pk':self.pk})
    class Meta:
        ordering = ["date"]

class TripPayment(models.Model):
    date = models.DateField(default=date.today)
    amount = models.DecimalField(max_digits=19,decimal_places=2)
    transaction = models.ForeignKey(Transaction,related_name='TripPayments',on_delete=models.PROTECT)
    inout_type = models.CharField(max_length=25,choices=[('DR','Debit'),('CR','Credit')])
    booking = models.ForeignKey(Booking,related_name='TripPayments',on_delete=models.PROTECT)
    description = models.ForeignKey(TripPaymentHead,related_name='TripPayments',on_delete=models.PROTECT,blank=False)
    vendor = models.ForeignKey(Vendor,related_name='TripPayments',on_delete=models.PROTECT,blank=True,null=True)
    # description_choices = [
    #     ('NONE','Please Select Description'),
    #     ('CUSTOMERIN','Customer In-Payment'),
    #     ('CUSTOMERREF','Customer Refund'),
    #     ('FLIGHT','Flight'),
    #     ('TRAIN','Train'),
    #     ('HOTEL','Hotel'),
    #     ('VISA','Visa'),
    #     ('TI','Travel Insurance'),
    #     ('LP','Land Package'),
    #     ('FERRY','Ferry'),
    #     ('BUS','Bus'),
    #     ('COMMOUT','Commission Paid'),
    #     ('COMMIN','Commission Received'),
    # ]
    def __str__(self):
        display_name =  '{} ({} Rs)'.format(self.booking, self.amount)
        return display_name

class PendingPayment(models.Model):
    date = models.DateField()
    amount = models.DecimalField(max_digits=19,decimal_places=2)
    inout_type = models.CharField(max_length=25,choices=[('DR','Debit'),('CR','Credit')])
    booking = models.ForeignKey(Booking,related_name='PendingPayments',on_delete=models.PROTECT)
    vendor = models.ForeignKey(Vendor,related_name='PendingPayments',on_delete=models.PROTECT,blank=True,null=True)
