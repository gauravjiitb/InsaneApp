from django.shortcuts import render
from django.contrib.auth.mixins import LoginRequiredMixin,UserPassesTestMixin
from django.views.generic import TemplateView,ListView,DetailView,CreateView,UpdateView
from django_filters.views import FilterView

from OperationsApp.models import Booking
from OperationsApp.forms import BookingForm
from OperationsApp.filters import BookingFilter

###############################
#   CUSTOMER VIEWS
###############################

class BookingListView(LoginRequiredMixin,FilterView):
    template_name = 'OperationsApp/booking_list.html'
    paginate_by = 5
    form_class = BookingForm
    filterset_class = BookingFilter

class BookingDetailView(DetailView):
    model = Booking

class BookingCreateView(LoginRequiredMixin,UserPassesTestMixin,CreateView):
    # redirect_field_name = 'SalesApp/customer_detail.html'
    form_class = BookingForm
    model = Booking
    def test_func(self):
        return self.request.user.groups.filter(name='Operations').exists()

class BookingUpdateView(LoginRequiredMixin,UserPassesTestMixin,UpdateView):
    # redirect_field_name = 'SalesApp/customer_detail.html'
    form_class = BookingForm
    model = Booking
    def test_func(self):
        return self.request.user.groups.filter(name='Operations').exists()
