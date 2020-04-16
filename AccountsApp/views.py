from django.shortcuts import render,redirect
from django.http import HttpResponseRedirect
from django.contrib.auth.mixins import LoginRequiredMixin,UserPassesTestMixin
from django.views.generic import TemplateView,ListView,DetailView,CreateView,UpdateView,DeleteView
from django.urls import reverse_lazy,reverse
from django_filters.views import FilterView
from django.views.generic.edit import ModelFormMixin
from django.forms import formset_factory
from django.contrib.auth.decorators import user_passes_test

from SalesApp.models import Customer,Lead
from OperationsApp.models import Booking
from AccountsApp.models import Account,TransactionHead,Transaction,TripPayment,PendingPayment
from AccountsApp.filters import TransactionFilter,TripPaymentFilter
from AccountsApp.forms import TransactionForm,PendingPaymentFormSet,TransactionUploadFormSet,TripPaymentFormSet,TripPaymentForm
from AccountsApp import helper_functions as acc_helpers

#######################################################
# HELPER FUNCTIONS
def accounts_group_check(user):
    return user.groups.filter(name='Accounts').exists() or user.is_superuser

def sales_group_check(user):
    return user.groups.filter(name='Sales').exists() or user.is_superuser
#######################################################



# Create your views here.

class TransactionListView(LoginRequiredMixin,FilterView):
    template_name = 'AccountsApp/transaction_list.html'
    paginate_by = 10
    form_class = TransactionForm
    filterset_class = TransactionFilter
    ordering = ['date']

class TransactionDetailView(LoginRequiredMixin,DetailView):
    model = Transaction
    def get_context_data(self,**kwargs):
        context = super(TransactionDetailView,self).get_context_data(**kwargs)
        primary_key = self.kwargs.get('pk')
        context['trip_payments'] = TripPayment.objects.filter(transaction = primary_key)
        return context

class TransactionCreateView(LoginRequiredMixin,UserPassesTestMixin,CreateView):
    form_class = TransactionForm
    model = Transaction
    def test_func(self):
        return self.request.user.groups.filter(name='Accounts').exists()

class TransactionUpdateView(LoginRequiredMixin,UserPassesTestMixin,UpdateView):
    form_class = TransactionForm
    model = Transaction
    context_object_name = 'transaction'
    def get_context_data(self,**kwargs):
        context = super(TransactionUpdateView,self).get_context_data(**kwargs)
        context['update'] = True
        return context
    def test_func(self):
        return self.request.user.groups.filter(name='Accounts').exists()



# THIS VIEW HANDELS THE BULK-UPLOAD OF FROM FILES DOWNLOADED FROM BANK PORTAL.
@user_passes_test(accounts_group_check,login_url='error403')
def transaction_upload(request):
    template_name = 'AccountsApp/transaction_upload_form.html'
    error = ''
    if request.method == 'POST':
        if request.FILES: # FILEPATH PRESENT
                uploaded_file = request.FILES['document']
                print('FILEPATH PRESENT')
                if uploaded_file.size < 104858:
                    transactions,num_transactions,valid,parsing_error = acc_helpers.hdfc_transaction_txtfile_parser(uploaded_file)
                    # HEADER: 0-date 1-reconcile_details 2-reference 4-debitamount 5-creditamount 6-reference_num 7-balance
                    if valid:
                        file_valid = True
                        # Process the transactions further
                        for transaction in transactions:
                            type, num_trips,trip_list = acc_helpers.parse_hdfc_reconcile_details(transaction['reconcile_details'])

                            inout_type = 'CR' if transaction['debitamount'] == 0 else 'DR'
                            amount = transaction['debitamount'] if inout_type == 'DR' else transaction['creditamount']
                            transaction.update({'inout_type':inout_type})
                            transaction.update({'amount':amount})

                            if type == 'ncnv':
                                transaction.update({'description':transaction['reconcile_details']})
                            else:
                                description = ''
                                for trip in trip_list:
                                    trip_id = trip[0].upper()
                                    amount = trip[1]
                                    booking = Booking.objects.get(trip_id=trip_id)
                                    name = booking.lead.customer.name
                                    description += trip_id + " "+ name + " (" + amount + " Rs),  "
                                transaction.update({'description':description})

                        # ------- FORM PROCESSING ------------------
                        formset = TransactionUploadFormSet(initial=transactions)
                        form_error = ''

                        return render(request,template_name,{'file_valid':file_valid,'formset':formset,'form_error':form_error})
                    else:   # raises error if unable to parse the file, and redirects file upload again
                        error = parsing_error
                else:
                    error = 'Uploaded file size is more than 100 KB. Please upload another file.'
        else:
            # NO FILEPATH PRESENT
            formset = TransactionUploadFormSet(request.POST)
            formset.is_valid()
            # Save to forms to create transactions
            account = Account.objects.get(name='HDFC')
            for form in formset:
                date = form.cleaned_data.get('date')
                amount = form.cleaned_data.get('amount')
                transaction_head = form.cleaned_data.get('transaction_head')
                transaction_ref = form.cleaned_data.get('reference')
                reference_number = form.cleaned_data.get('reference_num')
                description = form.cleaned_data.get('description')
                inout_type = form.cleaned_data.get('inout_type')
                balance = form.cleaned_data.get('balance')
                remarks = form.cleaned_data.get('remarks')
                reconcile_details = form.cleaned_data.get('reconcile_details')
                # reconcile_status_bool = form.cleaned_data.get('reconcile_bool')
                reconcile_status_bool = False if transaction_head.trip_bool == True else True
                Transaction.objects.create(date=date, account=account, transaction_ref=transaction_ref, amount=amount, reference_number=reference_number, description=description, inout_type=inout_type, balance=balance, transaction_head=transaction_head, remarks=remarks, reconcile_details=reconcile_details, reconcile_status_bool=reconcile_status_bool)
            return HttpResponseRedirect(reverse('AccountsApp:transaction_list'))
    return render(request,template_name,{'error':error})



# THIS VIEW HANDELS THE RECONCILIATION OF TRANSACTIONS.
@user_passes_test(accounts_group_check,login_url='error403')
def transaction_reconcile(request,pk):
    template_name = 'AccountsApp/transaction_reconcile.html'
    error = ''
    formset_error = ''
    payments_list = []

    transaction = Transaction.objects.get(id=pk)
    type, num_trips,trip_list = acc_helpers.parse_hdfc_reconcile_details(transaction.reconcile_details)
    date = transaction.date

    # CHECKS IF THE TRANSACTION IS CUSTOMER/VENDOR RELATED. (ncnv = Neither Customer Nor Vendor). Also checks if there is any error in the reconciliation data.
    try:
        total_reconciled_amount = 0
        for trip in trip_list:
            trip_id = trip[0].upper()
            inout_type = 'CR' if (type == 'c'and float(trip[1]) > 0) or (type == 'v'and float(trip[1]) < 0) else 'DR'
            total_reconciled_amount += float(trip[1])
            amount = abs(float(trip[1]))
            booking = Booking.objects.get(trip_id=trip_id)
            payments_list.append({'date':date,'transaction':transaction,'amount':amount,'inout_type':inout_type,'booking':booking})
        if total_reconciled_amount != transaction.amount:
            error = "Either you're trying to reconcile a non-trip transaction OR something is wrong with the reconciliation details in your transaction. Please check again."
            return render(request,template_name,{'error':error,'type':type})
    except:
        error = "Either you're trying to reconcile a non-trip transaction OR something is wrong with the reconciliation details in your transaction. Please check again."
        return render(request,template_name,{'error':error,'type':type})

    if request.method == 'POST':
        formset = TripPaymentFormSet(request.POST)
        if formset.is_valid():
            for form in formset:
                amount = form.cleaned_data.get('amount')
                inout_type = form.cleaned_data.get('inout_type')
                booking = form.cleaned_data.get('booking')
                description = form.cleaned_data.get('description')
                vendor = form.cleaned_data.get('vendor')
                TripPayment.objects.create(date=date,transaction=transaction,amount=amount,inout_type=inout_type,booking=booking,description=description,vendor=vendor)
                # UPDATE PENDING PAYMENTS
                if inout_type == 'CR' and not vendor: # PENDING PAYMENTS ARE ONLY MAINTAINED FOR CUSTOMER IN-PAYMENTS
                    pending_payments = PendingPayment.objects.filter(booking=booking,vendor__isnull=True).order_by('date')
                    for pending_payment in pending_payments:
                        if pending_payment.amount <= amount:
                            amount -= pending_payment.amount
                            pending_payment.delete()
                        else:
                            pending_payment.amount -= amount
                            pending_payment.save(update_fields=['amount'])
            transaction.reconcile_status_bool = True
            transaction.save(update_fields=['reconcile_status_bool'])
            return HttpResponseRedirect(reverse('AccountsApp:transaction_detail', kwargs={'pk':pk}))
        else:
            formset_error = 'There is something wrong with the values entered by you. Please try again.'
    else: # POPULATES INITIAL DATA
        formset = TripPaymentFormSet(initial=payments_list)
    return render(request,template_name,{'formset':formset,'formset_error':formset_error,'type':type})



# THIS VIEW CANCELS THE RECONCILIATION OF A TRANSACTION.
@user_passes_test(accounts_group_check,login_url='error403')
def transaction_reconcile_cancel(request,pk):
    template_name = 'AccountsApp/transaction_reconcile_cancel.html'
    if request.method == 'POST':
        transaction = Transaction.objects.get(id=pk)
        trip_payments = TripPayment.objects.filter(transaction=transaction)
        for payment in trip_payments:
            if payment.inout_type == 'CR' and not payment.vendor: # RUNS ONLY FOR CUSTOMER IN-PAYMENTS
                PendingPayment.objects.create(date=payment.date,amount=payment.amount,inout_type='CR',booking=payment.booking)
        trip_payments.delete()
        transaction.reconcile_status_bool = False
        transaction.save(update_fields=['reconcile_status_bool'])
        return HttpResponseRedirect(reverse('AccountsApp:transaction_list'))
    return render(request,template_name)



# THIS VIEW HANDELS THE CREATION AND UPDATION OF PENDING PAYMENTS FROM A CUSTOMER.
@user_passes_test(sales_group_check,login_url='error403')
def create_proforma_invoice(request,pk):
    template_name = 'AccountsApp/proforma_invoice_form.html'
    current_pending_payments_list = [{'date':PendingPayment.date,'amount':PendingPayment.amount} for PendingPayment in PendingPayment.objects.filter(booking__id=pk).order_by('date')]
    form_error = ""

    if request.method == 'POST':
        formset = PendingPaymentFormSet(request.POST)
        if formset.is_valid(): # will filter out invalid/incomplete forms, but let empty forms pass
            PendingPayment.objects.filter(booking = pk).delete() # delete existing related pending payments
            booking = Booking.objects.get(id=pk)
            for form in formset:
                if form.cleaned_data.get('amount'): # just check for any one field to filter out empty forms
                    date = form.cleaned_data.get('date')
                    amount = form.cleaned_data.get('amount')
                    PendingPayment.objects.create(date=date,amount=amount,inout_type='CR',booking=booking)
            return HttpResponseRedirect(reverse('OperationsApp:booking_detail', kwargs={'pk':pk}))
        else:
            form_error = "VALIDATION ERROR : Please enter valid details."
            formset = PendingPaymentFormSet(initial=current_pending_payments_list)
    else:
        formset = PendingPaymentFormSet(initial=current_pending_payments_list)
    return render(request,template_name,{'formset':formset,'form_error':form_error})



class TripPaymentListView(LoginRequiredMixin,FilterView):
    template_name = 'AccountsApp/trippayment_list.html'
    paginate_by = 10
    form_class = TripPaymentForm
    filterset_class = TripPaymentFilter
    ordering = ['booking']
