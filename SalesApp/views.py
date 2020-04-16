from django.shortcuts import render
from django.contrib.auth.mixins import LoginRequiredMixin,UserPassesTestMixin
from django.views.generic import TemplateView,ListView,DetailView,CreateView,UpdateView,DeleteView
from django.urls import reverse_lazy
# from django.contrib.auth.decorators import user_passes_test
from django_filters.views import FilterView
from django.views.generic.edit import ModelFormMixin

from SalesApp.models import Customer,Lead
from OperationsApp.models import Booking
from SalesApp.forms import CustomerForm,LeadForm,LeadFromCustomerForm
from SalesApp.filters import CustomerFilter,LeadFilter

###############################
#   CUSTOMER VIEWS
###############################

class CustomerListView(LoginRequiredMixin,FilterView):
    template_name = 'SalesApp/customer_list.html'
    paginate_by = 10
    form_class = CustomerForm
    filterset_class = CustomerFilter
    ordering = ['id']
    # queryset = Customer.objects.order_by('id')
    # context_object_name = 'customer_list'



class CustomerDetailView(DetailView):
    model = Customer
    # context_object_name = 'customer'
    def get_context_data(self,**kwargs):
        context = super(CustomerDetailView,self).get_context_data(**kwargs)
        primary_key = self.kwargs.get('pk')
        context['leads'] = Lead.objects.filter(customer = primary_key)
        context['bookings'] = Booking.objects.filter(customer = primary_key)
        return context
	# def get_queryset(self):
	# 	if self.request.user.is_authenticated:
	# 		return Customer.objects.filter(user=self.request.user)

class CustomerCreateView(LoginRequiredMixin,UserPassesTestMixin,CreateView):
    # redirect_field_name = 'SalesApp/customer_detail.html'
    form_class = CustomerForm
    model = Customer
    def test_func(self):
        return self.request.user.groups.filter(name='Sales').exists()

class CustomerUpdateView(LoginRequiredMixin,UserPassesTestMixin,UpdateView):
    form_class = CustomerForm
    model = Customer
    def test_func(self):
        return self.request.user.groups.filter(name='Sales').exists()

# class CustomerDeleteView(LoginRequiredMixin,UserPassesTestMixin,DeleteView):
#     model = Customer
#     success_url = reverse_lazy('SalesApp:customer_list')
#     def test_func(self):
#         return self.request.user.is_superuser


###############################
#   LEAD VIEWS
###############################
class LeadListView(LoginRequiredMixin,FilterView):
    """ Generates a view to see details of all leads in a list. """
    template_name = 'SalesApp/lead_list.html'
    paginate_by = 10
    form_class = LeadForm
    filterset_class = LeadFilter
    ordering = ['id']

class LeadDetailView(LoginRequiredMixin,DetailView):
    model = Lead
    def get_context_data(self,**kwargs):
        context = super(LeadDetailView,self).get_context_data(**kwargs)
        primary_key = self.kwargs.get('pk')
        context['bookings'] = Booking.objects.filter(lead = primary_key)
        return context

class LeadCreateView(LoginRequiredMixin,UserPassesTestMixin,CreateView):
    form_class = LeadForm
    model = Lead
    def get_initial(self):
        """
        Returns the initial data to use for forms on this view.
        """
        initial = super().get_initial()
        try:
            customer_id = self.request.GET.get("customer_id")
            initial['customer'] = Customer.objects.get(id=customer_id)
        except:
            pass
        return initial

    def test_func(self):
        return self.request.user.groups.filter(name='Sales').exists()



class LeadUpdateView(LoginRequiredMixin,UserPassesTestMixin,UpdateView):
    form_class = LeadForm
    model = Lead
    def test_func(self):
        return self.request.user.groups.filter(name='Sales').exists()

# class LeadCreateFromCustomerView(LoginRequiredMixin,UserPassesTestMixin,CreateView):
#     form_class = LeadForm
#     model = Lead
#     def test_func(self):
#         return self.request.user.groups.filter(name='Sales').exists()
#     # def form_valid(self,form):
#     #     customer_id = self.request.GET.get("value")
#     #     form.instance.customer = Customer.objects.get(id=customer_id)
#     #     return super(LeadCreateFromCustomerView,self).form_valid(form)
#     def get_initial(self):
#         """
#         Returns the initial data to use for forms on this view.
#         """
#         initial = super().get_initial()
#         customer_id = self.request.GET.get("customer_id")
#         initial['customer'] = Customer.objects.get(id=customer_id)
#         return initial
