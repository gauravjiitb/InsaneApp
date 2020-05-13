from django.contrib import admin
from django.urls import path,include

from AccountsApp import views
from AccountsApp.models import Account,TransactionHead,Transaction,TripPayment,PendingPayment

app_name = 'AccountsApp'

urlpatterns = [
    path('transaction/list/',views.TransactionListView.as_view(),name='transaction_list'),
    path('transaction/<int:pk>/detail/',views.TransactionDetailView.as_view(),name='transaction_detail'),
    path('transaction/create/',views.TransactionCreateView.as_view(),name='transaction_create'),
    path('transaction/<int:pk>/update/',views.TransactionUpdateView.as_view(),name='transaction_update'),
    path('transaction/upload/',views.transaction_upload,name='transaction_upload'),
    path('transaction/<int:pk>/reconcile/',views.transaction_reconcile,name='transaction_reconcile'),
    path('transaction/<int:pk>/reconcile-cancel/',views.transaction_reconcile_cancel,name='transaction_reconcile_cancel'),
    # path('proforma-invoice/list/',views.ProformaInvoiceListView.as_view(),name='proforma_invoice_list'),
    path('booking/<int:pk>/proforma-invoice/',views.create_proforma_invoice,name='proforma_invoice_create_update'),
    path('trip-payments/',views.TripPaymentListView.as_view(),name='trippayment_list'),

    path('ajax/pending-payment/<int:pk>/send-reminder/',views.customer_payment_reminder,name='customer_payment_reminder'),
]
