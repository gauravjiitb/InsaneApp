from django.shortcuts import render
from django.contrib.auth.mixins import LoginRequiredMixin,UserPassesTestMixin
from django.views.generic import TemplateView,ListView,DetailView,CreateView,UpdateView,DeleteView
from django.urls import reverse_lazy
from django.contrib.auth.decorators import user_passes_test
from django_filters.views import FilterView

from SalesApp.models import Customer,Lead
from SalesApp.forms import CustomerForm,LeadForm,LeadFromCustomerForm
from SalesApp.filters import CustomerFilter,LeadFilter

###############################
#   CUSTOMER VIEWS
###############################

class CustomerListView(LoginRequiredMixin,FilterView):
    template_name = 'SalesApp/customer_list.html'
    paginate_by = 3
    form_class = CustomerForm
    filterset_class = CustomerFilter


# ALTERNATE METHOD FOR FilterView
# def sales_group_check(user):
#     return user.groups.filter(name='Sales').exists() or user.is_superuser
#
# @user_passes_test(sales_group_check,login_url='error403')
# def customer_list(request):
#     f = CustomerFilter(request.GET, queryset=Customer.objects.all())
#     return render(request, 'SalesApp/customer_list.html', {'filter': f})

class CustomerDetailView(DetailView):
    model = Customer

class CustomerCreateView(LoginRequiredMixin,UserPassesTestMixin,CreateView):
    # redirect_field_name = 'SalesApp/customer_detail.html'
    form_class = CustomerForm
    model = Customer
    def test_func(self):
        return self.request.user.groups.filter(name='Sales').exists()

class CustomerUpdateView(LoginRequiredMixin,UserPassesTestMixin,UpdateView):
    # redirect_field_name = 'SalesApp/customer_detail.html'
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
    template_name = 'SalesApp/lead_list.html'
    paginate_by = 3
    form_class = LeadForm
    filterset_class = LeadFilter

class LeadDetailView(DetailView):
    model = Lead

class LeadCreateView(LoginRequiredMixin,UserPassesTestMixin,CreateView):
    form_class = LeadForm
    model = Lead
    def test_func(self):
        return self.request.user.groups.filter(name='Sales').exists()

class LeadUpdateView(LoginRequiredMixin,UserPassesTestMixin,UpdateView):
    form_class = LeadForm
    model = Lead
    def test_func(self):
        return self.request.user.groups.filter(name='Sales').exists()

# class LeadDeleteView(LoginRequiredMixin,UserPassesTestMixin,DeleteView):
#     model = Lead
#     success_url = reverse_lazy('SalesApp:lead_list')
#     def test_func(self):
#         return self.request.user.is_superuser

class LeadCreateFromCustomerView(LoginRequiredMixin,UserPassesTestMixin,CreateView):
    form_class = LeadFromCustomerForm
    model = Lead
    def test_func(self):
        return self.request.user.groups.filter(name='Sales').exists()
    def form_valid(self,form):
        form.instance.customer = Customer.objects.get(id=self.request.pk)
        return super().form_valid(form)
