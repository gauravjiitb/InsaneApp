from django.shortcuts import render,redirect
from django.contrib.auth.mixins import LoginRequiredMixin,UserPassesTestMixin
from django.views.generic import FormView,ListView,DetailView, CreateView
from django.urls import reverse_lazy,reverse
from django.contrib.auth import get_user_model

from django_filters.views import FilterView

from ProfilesApp.models import Customer, Traveler, Staff
from SalesApp.models import Lead
from OperationsApp.models import Booking
from ProfilesApp.forms import CustomerCreateForm,CustomerUpdateForm, TravelerForm
from ProfilesApp.filters import CustomerFilter


# Create your views here.


###############################
#   CUSTOMER VIEWS
###############################
class CustomerListView(LoginRequiredMixin,FilterView):
    template_name = 'ProfilesApp/customer_list.html'
    paginate_by = 10
    form_class = CustomerCreateForm
    filterset_class = CustomerFilter
    ordering = ['id']


class CustomerDetailView(LoginRequiredMixin,DetailView):
    model = Customer
    context_object_name = 'customer'
    def get_context_data(self,**kwargs):
        context = super(CustomerDetailView,self).get_context_data(**kwargs)
        pk = self.kwargs.get('pk')
        customer = Customer.objects.get(id=pk)
        context['leads'] = Lead.objects.filter(customer = customer)
        context['bookings'] = Booking.objects.filter(quote__lead__customer = customer)
        return context


class CustomerCreateView(LoginRequiredMixin,FormView):
    form_class = CustomerCreateForm
    template_name = 'ProfilesApp/customer_form.html'

    def form_valid(self,form):
        form.save()
        return redirect('ProfilesApp:customer_list')


class CustomerUpdateView(LoginRequiredMixin,FormView):
    form_class = CustomerUpdateForm
    template_name = 'ProfilesApp/customer_form.html'

    def form_valid(self,form):
        pk = self.kwargs.get('pk')
        user = form.save(pk=pk)
        return redirect('ProfilesApp:customer_detail', pk=pk)

    def get_initial(self):
        initial = super().get_initial()
        pk = self.kwargs.get('pk')
        customer = Customer.objects.get(id=pk)
        initial['email'] = customer.user.email
        initial['name'] = customer.user.name
        initial['phone'] = customer.user.phone
        return initial


###############################
#   TRAVELER VIEWS
###############################

class TravelerCreateView(LoginRequiredMixin,CreateView):
    model = Traveler
    form_class = TravelerForm

class TravelerUpdateView(LoginRequiredMixin,CreateView):
    model = Traveler
    form_class = TravelerForm
