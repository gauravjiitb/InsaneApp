from django.shortcuts import render, HttpResponseRedirect
from django.contrib.auth.mixins import LoginRequiredMixin,UserPassesTestMixin
from django.views.generic import TemplateView,ListView,DetailView,CreateView,UpdateView,DeleteView
from django.urls import reverse_lazy,reverse
# from django.contrib.auth.decorators import user_passes_test
from django_filters.views import FilterView
from django.views.generic.edit import ModelFormMixin
from bootstrap_modal_forms.generic import BSModalCreateView,BSModalUpdateView

from SalesApp.models import Lead,Quote,QuoteHotelInfo,QuoteTransferInfo,QuoteSightseeingInfo
from ProfilesApp.models import Customer
from OperationsApp.models import Booking
from ContentApp.models import Destination,City, Hotel, Transfer, Sightseeing
from SalesApp.forms import LeadForm, QuoteForm, QuotePaxDetailForm, QuotePlacesDetailForm,QuoteHotelInfoFormSet,QuoteTransferInfoFormSet,QuoteSightseeingInfoFormSet
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


###############################
#   QUOTE VIEWS
###############################

# HELPER FUNCTIONS FOR QUOTE

def quote_load_cities(request):
    template_name = 'SalesApp/quote_form/city_dropdown_list_options.html'
    destination_ids = request.GET.getlist('destinations[]')
    destinations = Destination.objects.filter(pk__in=destination_ids)
    cities = City.objects.filter(destination__in=destinations).order_by('name')
    return render(request, template_name, {'cities': cities})

def quote_load_hotels(request):
    city_id = request.GET.get('city_id')
    hotels = Hotel.objects.filter(city__id=city_id).order_by('name')
    return render(request, 'SalesApp/quote_form/hotels_dropdown_options.html', {'hotels': hotels})

def quote_load_transfers(request):
    city_id = request.GET.get('city_id')
    transfers = Transfer.objects.filter(city__id=city_id).order_by('name')
    return render(request, 'SalesApp/quote_form/transfers_dropdown_options.html', {'transfers': transfers})

def quote_load_sightseeings(request):
    city_id = request.GET.get('city_id')
    sightseeings = Sightseeing.objects.filter(city__id=city_id).order_by('name')
    return render(request, 'SalesApp/quote_form/sightseeings_dropdown_options.html', {'sightseeings': sightseeings})

def quote_pax_details(request):
    template_name = 'SalesApp/quote_form/pax_details.html'
    if request.method == 'POST':
        pass
    else:
        pax_form = QuotePaxDetailForm()
        places_form = QuotePlacesDetailForm()
    return render(request,template_name,{'pax_form':pax_form,'places_form':places_form})

###############################

def quote_create(request,pk=None):
    template_name = 'SalesApp/quote_form.html'
    initial_quote = Quote.objects.get(id=pk) if pk else None

    if request.method == 'POST':
        form = QuoteForm(request.POST,instance=initial_quote)
        hotel_formset = QuoteHotelInfoFormSet(request.POST,prefix='hotel')
        transfer_formset = QuoteTransferInfoFormSet(request.POST,prefix='transfer')
        sightseeing_formset = QuoteSightseeingInfoFormSet(request.POST,prefix='sightseeing')
        # if not form.is_valid():
        #     print('FORM NOT VALID')
        #     print(form.errors)
        # if not hotel_formset.is_valid():
        #     print('HOTEL FORMSET NOT VALID')
        # if not transfer_formset.is_valid():
        #     print('TRANSFER FORMSET NOT VALID')

        if form.is_valid() and hotel_formset.is_valid() and transfer_formset.is_valid() and sightseeing_formset.is_valid():
            print('FORM, HOTEL FORMSET, TRANSFER FORMSETn SIGHTSEEING FORMSET ARE VALID.')
            quote = form.save()

            hotels = hotel_formset.save(commit=False)
            for hotel in hotels:
                hotel.quote = quote
            hotel_formset.save()

            transfers = transfer_formset.save(commit=False)
            for transfer in transfers:
                transfer.quote = quote
            transfer_formset.save()

            sightseeings = sightseeing_formset.save(commit=False)
            for sightseeing in sightseeings:
                sightseeing.quote = quote
            sightseeing_formset.save()

            return HttpResponseRedirect(reverse('dashboard'))
    else:
        form = QuoteForm(instance=initial_quote)
        hotel_formset = QuoteHotelInfoFormSet(queryset=QuoteHotelInfo.objects.filter(quote=initial_quote),prefix='hotel')
        transfer_formset = QuoteTransferInfoFormSet(queryset=QuoteTransferInfo.objects.filter(quote=initial_quote),prefix='transfer')
        sightseeing_formset = QuoteSightseeingInfoFormSet(queryset=QuoteSightseeingInfo.objects.filter(quote=initial_quote),prefix='sightseeing')
    return render(request, template_name, {'form':form,'hotel_formset':hotel_formset,'transfer_formset':transfer_formset,'sightseeing_formset':sightseeing_formset})


# class QuoteCreateView(CreateView):
#     model = Quote
#     form_class = QuoteForm
#     success_url = reverse_lazy('dashboard')
#
#     def get_initial(self):
#         """  Returns the initial data to use for forms on this view. """
#         initial = super().get_initial()
#         try:
#             lead_id = self.request.GET.get("lead_id")
#             initial['lead'] = Lead.objects.get(id=lead_id)
#         except:
#             pass
#         return initial

#
#
# class QuoteUpdateView(UpdateView):
#     model = Quote
#     form_class = QuoteForm
#     success_url = reverse_lazy('dashboard')
