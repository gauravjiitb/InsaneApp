from django.shortcuts import render
from django.contrib.auth.mixins import LoginRequiredMixin,UserPassesTestMixin
from django.views.generic import TemplateView,ListView,DetailView,CreateView,UpdateView,DeleteView
from django.urls import reverse_lazy,reverse
# from django.contrib.auth.decorators import user_passes_test
from django_filters.views import FilterView
from django.views.generic.edit import ModelFormMixin
from bootstrap_modal_forms.generic import BSModalCreateView,BSModalUpdateView

from SalesApp.models import Lead
from ProfilesApp.models import Customer
from OperationsApp.models import Booking
from SalesApp.forms import LeadForm
from SalesApp.filters import LeadFilter



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
