from django.shortcuts import render
from django.contrib.auth.mixins import LoginRequiredMixin,UserPassesTestMixin
from django.views.generic import TemplateView,ListView,DetailView,CreateView,UpdateView
from django_filters.views import FilterView
from itertools import chain

from OperationsApp.models import Booking
from SalesApp.models import Lead
from OperationsApp.forms import BookingForm
from OperationsApp.filters import BookingFilter
from AccountsApp.models import PendingPayment,TripPayment

###############################
#   CUSTOMER VIEWS
###############################

class BookingListView(LoginRequiredMixin,FilterView):
    template_name = 'OperationsApp/booking_list.html'
    paginate_by = 5
    form_class = BookingForm
    filterset_class = BookingFilter



class BookingDetailView(LoginRequiredMixin,DetailView):
    model = Booking
    context_object_name = 'booking'

    def get_context_data(self,**kwargs):
        context = super(BookingDetailView,self).get_context_data(**kwargs)
        primary_key = self.kwargs.get('pk')
        pending_payments = PendingPayment.objects.filter(booking = primary_key,vendor__isnull=True)
        trip_payments = TripPayment.objects.filter(booking = primary_key,vendor__isnull=True)
        context['payments'] = sorted(chain(pending_payments, trip_payments),key=lambda data: data.date)
        return context



class BookingCreateView(LoginRequiredMixin,UserPassesTestMixin,CreateView):
    # redirect_field_name = 'SalesApp/customer_detail.html'
    form_class = BookingForm
    model = Booking

    def get_initial(self):
        """
        Returns the initial data to use for forms on this view.
        """
        initial = super().get_initial()
        try:
            lead_id = self.request.GET.get("lead_id")
            initial['lead'] = Lead.objects.get(id=lead_id)
        except:
            pass
        return initial

    def test_func(self):
        return self.request.user.groups.filter(name='Operations').exists()



class BookingUpdateView(LoginRequiredMixin,UserPassesTestMixin,UpdateView):
    # redirect_field_name = 'SalesApp/customer_detail.html'
    form_class = BookingForm
    model = Booking
    def test_func(self):
        return self.request.user.groups.filter(name='Operations').exists()
