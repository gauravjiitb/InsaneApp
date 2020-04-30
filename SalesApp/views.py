from django.shortcuts import render, HttpResponseRedirect
from django.contrib.auth.mixins import LoginRequiredMixin,UserPassesTestMixin
from django.views.generic import TemplateView,ListView,DetailView,CreateView,UpdateView
from django.urls import reverse_lazy,reverse
from datetime import timedelta

from django_filters.views import FilterView

from SalesApp.models import (Lead,Quote,QuoteFlightInfo,
                                        QuoteTransportInfo,
                                        QuoteHotelInfo,
                                        QuoteTransferInfo,
                                        QuoteSightseeingInfo,
                                        QuoteVisaInfo,
                                        QuoteInsuranceInfo,
                                        QuoteItineraryInfo,
                                        QuoteOthersInfo)
from ProfilesApp.models import Customer
from OperationsApp.models import Booking
from ContentApp.models import Destination,City, Hotel, Transfer, Sightseeing
from SalesApp.filters import LeadFilter
from SalesApp.forms import (LeadForm, QuoteForm,
                                      QuoteFlightInfoFormSet,
                                      QuoteTransportInfoFormSet,
                                      QuoteHotelInfoFormSet,
                                      QuoteTransferInfoFormSet,
                                      QuoteSightseeingInfoFormSet,
                                      QuoteVisaInfoFormSet,
                                      QuoteInsuranceInfoFormSet,
                                      QuoteItineraryInfoFormSet,
                                      QuoteOthersInfoFormSet)




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


###############################

def quote_create_update(request,pk=None):
    template_name = 'SalesApp/quote_form.html'
    initial_quote = Quote.objects.get(id=pk) if pk else None
    itinerary_objects_list = []
    itinerary_choices_objects_list = []

    # TRANSLATES THE ITINERARY ORDERING INTO OBJECTS LISTS
    def create_itinerary_lists(initial_quote,ordering_list=None):
        itinerary_objects_list = []
        itinerary_choices_objects_list = []
        if not initial_quote.quoteitineraryinfo_set.all():
            duration = (initial_quote.end_date - initial_quote.start_date).days + 1
            date = initial_quote.start_date
            for i in range(duration):
                QuoteItineraryInfo.objects.create(quote=initial_quote,date=date)
                date = date + timedelta(days=1)
                itinerary_objects_list.append([])
            itinerary_choices_objects_list = list(initial_quote.quotetransferinfo_set.all()) + list(initial_quote.quotesightseeinginfo_set.all())
        else:
            transfer_qs_remove_ids = []
            sightseeing_qs_remove_ids = []
            if ordering_list is None:
                ordering_list = []
                for object in initial_quote.quoteitineraryinfo_set.all():
                    ordering_list.append(object.ordering)
            for ordering in ordering_list:
                items = ordering.split(',')
                object_list = []
                for item in items:
                    if item:
                        x = item.split('-')
                        object_type = x[0]
                        id = int(x[1])
                        if object_type == 'transfer':
                            try: # THIS WILL CHECK IF THE QUOTE-ITINERARY OBJECT HAS BEEN DELETED, OTHERWISE ADD IT TO DISPLAY LIST
                                object_list.append(QuoteTransferInfo.objects.get(id=id))
                                transfer_qs_remove_ids.append(id)
                            except:
                                pass
                        else:
                            try: # THIS WILL CHECK IF THE QUOTE-SIGHTSEEING OBJECT HAS BEEN DELETED, OTHERWISE ADD IT TO DISPLAY LIST
                                object_list.append(QuoteSightseeingInfo.objects.get(id=id))
                                sightseeing_qs_remove_ids.append(id)
                            except:
                                pass
                itinerary_objects_list.append(object_list)
            transfer_choices_qs = QuoteTransferInfo.objects.filter(quote=initial_quote).exclude(id__in=transfer_qs_remove_ids)
            sightseeing_choices_qs = QuoteSightseeingInfo.objects.filter(quote=initial_quote).exclude(id__in=sightseeing_qs_remove_ids)
            itinerary_choices_objects_list = list(transfer_choices_qs) + list(sightseeing_choices_qs)
        return itinerary_objects_list,itinerary_choices_objects_list

    if request.method == 'POST':
        quote_form = QuoteForm(request.POST,instance=initial_quote)
        if quote_form.is_valid():
            quote = quote_form.save()
            initial = [{'quote':quote}]
        else:
            initial = []

        flight_formset = QuoteFlightInfoFormSet(request.POST,prefix='flight',initial=initial)
        transport_formset = QuoteTransportInfoFormSet(request.POST,prefix='transport',initial=initial)
        hotel_formset = QuoteHotelInfoFormSet(request.POST,prefix='hotel',initial=initial)
        transfer_formset = QuoteTransferInfoFormSet(request.POST,prefix='transfer',initial=initial)
        sightseeing_formset = QuoteSightseeingInfoFormSet(request.POST,prefix='sightseeing',initial=initial)
        visa_formset = QuoteVisaInfoFormSet(request.POST,prefix='visa',initial=initial)
        insurance_formset = QuoteInsuranceInfoFormSet(request.POST,prefix='insurance',initial=initial)
        others_formset = QuoteOthersInfoFormSet(request.POST,prefix='others',initial=initial)
        itinerary_formset = QuoteItineraryInfoFormSet(request.POST,prefix='itinerary',initial=initial)
        if itinerary_formset.is_valid(): # GETS THE ITINERARY ORDERING TO CONVERT THEM IN OBJECTS LIST FOR VIEW, IF THERE IS ERROR IN SAVING.
            ordering_list = []
            for form in itinerary_formset:
                ordering_list.append(form['ordering'].value())
            itinerary_objects_list,itinerary_choices_objects_list = create_itinerary_lists(initial_quote=initial_quote,ordering_list=ordering_list)

        if (quote_form.is_valid() and   flight_formset.is_valid() and
                                        transport_formset.is_valid() and
                                        hotel_formset.is_valid() and
                                        transfer_formset.is_valid() and
                                        sightseeing_formset.is_valid() and
                                        visa_formset.is_valid() and
                                        insurance_formset.is_valid() and
                                        others_formset.is_valid() and
                                        itinerary_formset.is_valid()):
            print('QUOTE FORM AND ALL FORMSETS ARE VALID.')

            flight_formset.save()
            transport_formset.save()

            # hotels = hotel_formset.save(commit=False)
            # for hotel in hotels:
            #     hotel.quote = quote
            hotel_formset.save()

            # transfers = transfer_formset.save(commit=False)
            # for transfer in transfers:
            #     transfer.quote = quote
            transfer_formset.save()

            # sightseeings = sightseeing_formset.save(commit=False)
            # for sightseeing in sightseeings:
            #     sightseeing.quote = quote
            sightseeing_formset.save()

            # visas = visa_formset.save(commit=False)
            # for visa in visas:
            #     visa.quote = quote
            visa_formset.save()

            # insurances = insurance_formset.save(commit=False)
            # for insurance in insurances:
            #     insurance.quote = quote
            insurance_formset.save()

            others_formset.save()

            # itineraries = itinerary_formset.save(commit=False)
            # for itinerary in itineraries:
            #     itinerary.quote = quote
            itinerary_formset.save()

            if request.POST.get('redirect') == 'False':
                return HttpResponseRedirect(reverse('SalesApp:quote_update', args=[quote.id]))
            else:
                return HttpResponseRedirect(reverse('dashboard'))
    else:
        try: # GET LEAD ID IF QUOTE CREATION REQUEST CAME FROM LEAD PAGE.
            lead_id = request.GET['lead_id']
        except:
            lead_id = None

        quote_form = QuoteForm(instance=initial_quote) if not lead_id else QuoteForm(initial={'lead':Lead.objects.get(id=lead_id)})
        flight_formset = QuoteFlightInfoFormSet(queryset=QuoteFlightInfo.objects.filter(quote=initial_quote),prefix='flight')
        transport_formset = QuoteTransportInfoFormSet(queryset=QuoteTransportInfo.objects.filter(quote=initial_quote),prefix='transport')
        hotel_formset = QuoteHotelInfoFormSet(queryset=QuoteHotelInfo.objects.filter(quote=initial_quote),prefix='hotel')
        transfer_formset = QuoteTransferInfoFormSet(queryset=QuoteTransferInfo.objects.filter(quote=initial_quote),prefix='transfer')
        sightseeing_formset = QuoteSightseeingInfoFormSet(queryset=QuoteSightseeingInfo.objects.filter(quote=initial_quote),prefix='sightseeing')
        visa_formset = QuoteVisaInfoFormSet(queryset=QuoteVisaInfo.objects.filter(quote=initial_quote),prefix='visa')
        insurance_formset = QuoteInsuranceInfoFormSet(queryset=QuoteInsuranceInfo.objects.filter(quote=initial_quote),prefix='insurance')
        others_formset = QuoteOthersInfoFormSet(queryset=QuoteOthersInfo.objects.filter(quote=initial_quote),prefix='others')
        itinerary_formset = QuoteItineraryInfoFormSet(queryset=QuoteItineraryInfo.objects.filter(quote=initial_quote),prefix='itinerary')
        if initial_quote:
            itinerary_objects_list,itinerary_choices_objects_list = create_itinerary_lists(initial_quote=initial_quote)
        # insurance_formset.extra = 2
    return render(request, template_name, {'itinerary_choices_objects_list':itinerary_choices_objects_list,
                                           'itinerary_objects_list':itinerary_objects_list,
                                           'quote_form':quote_form,
                                           'flight_formset':flight_formset,
                                           'transport_formset':transport_formset,
                                           'hotel_formset':hotel_formset,
                                           'transfer_formset':transfer_formset,
                                           'sightseeing_formset':sightseeing_formset,
                                           'visa_formset':visa_formset,
                                           'insurance_formset':insurance_formset,
                                           'others_formset':others_formset,
                                           'itinerary_formset':itinerary_formset})


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
