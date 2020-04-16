from django.contrib import admin
from AccountsApp.models import Account,TransactionHead,Transaction,TripPayment,PendingPayment,TripPaymentHead

# Register your models here.

admin.site.register(Account)
admin.site.register(TransactionHead)
admin.site.register(Transaction)
admin.site.register(TripPayment)
admin.site.register(PendingPayment)
admin.site.register(TripPaymentHead)
