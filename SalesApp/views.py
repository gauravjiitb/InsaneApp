from django.shortcuts import render, HttpResponseRedirect
from django.contrib.auth.mixins import LoginRequiredMixin,UserPassesTestMixin
from django.views.generic import TemplateView,ListView,DetailView,CreateView,UpdateView,FormView
from django.urls import reverse_lazy,reverse
from django.db.models import Q

from datetime import timedelta

from django_filters.views import FilterView

from SalesApp.models import (Lead,Quote,QuoteFlightInfo, QuoteTransportInfo, QuoteHotelInfo, QuoteTransferInfo, QuoteSightseeingInfo,
                                        QuoteVisaInfo, QuoteInsuranceInfo, QuoteItineraryInfo, QuoteOthersInfo, FlexInclusions,FlexItinerary)
from ProfilesApp.models import Customer
from OperationsApp.models import Booking
from ContentApp.models import Destination,City, Hotel, Transfer, Sightseeing
from SalesApp.filters import LeadFilter
from SalesApp.forms import (LeadForm, QuoteForm, QuoteFlightInfoFormSet, QuoteTransportInfoFormSet, QuoteHotelInfoFormSet, QuoteTransferInfoFormSet,
                            QuoteSightseeingInfoFormSet, QuoteVisaInfoFormSet, QuoteInsuranceInfoFormSet, QuoteItineraryInfoFormSet, QuoteOthersInfoFormSet,
                            FlexInclusionsForm, FlexItineraryForm)




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
    transfers = Transfer.objects.filter(city__id=city_id,price__gt=0).order_by('name')
    return render(request, 'SalesApp/quote_form/transfers_dropdown_options.html', {'transfers': transfers})

def quote_load_sightseeings(request):
    city_id = request.GET.get('city_id')
    sightseeings = Sightseeing.objects.filter(city__id=city_id,adult_price__gt=0,child_price__gt=0).order_by('name')
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
        cities = initial_quote.cities.all()
        if not initial_quote.quoteitineraryinfo_set.all():
            duration = (initial_quote.end_date - initial_quote.start_date).days + 1
            date = initial_quote.start_date
            for i in range(duration):
                QuoteItineraryInfo.objects.create(quote=initial_quote,date=date)
                date = date + timedelta(days=1)
                itinerary_objects_list.append([])
            itinerary_choices_objects_list = (list(initial_quote.quotetransferinfo_set.all())
                                                + list(initial_quote.quotesightseeinginfo_set.all())
                                                + list(Transfer.objects.filter(city__in=cities,price=0))
                                                + list(Sightseeing.objects.filter(city__in=cities,adult_price=0,child_price=0)))
        else:
            transfer_qs_remove_ids = []
            sightseeing_qs_remove_ids = []
            free_transfer_qs_remove_ids = []
            free_sightseeing_qs_remove_ids = []
            if ordering_list is None:
                ordering_list = []
                for object in initial_quote.quoteitineraryinfo_set.all():
                    ordering_list.append(object.ordering)
            for ordering in ordering_list:
                items = ordering.split(',')
                object_list = []
                for item in items:
                    if item:
                        [object_type,id] = item.split('-')
                        if object_type == 'transfer':
                            try: # THIS WILL CHECK IF THE QUOTE-ITINERARY OBJECT HAS BEEN DELETED, OTHERWISE ADD IT TO DISPLAY LIST
                                object_list.append(QuoteTransferInfo.objects.get(id=id))
                                transfer_qs_remove_ids.append(id)
                            except:
                                pass
                        elif object_type == 'sightseeing':
                            try: # THIS WILL CHECK IF THE QUOTE-SIGHTSEEING OBJECT HAS BEEN DELETED, OTHERWISE ADD IT TO DISPLAY LIST
                                object_list.append(QuoteSightseeingInfo.objects.get(id=id))
                                sightseeing_qs_remove_ids.append(id)
                            except:
                                pass
                        elif object_type == 'free_transfer':
                            tr = Transfer.objects.get(id=id)
                            if tr.city in cities:
                                object_list.append(tr)
                                free_transfer_qs_remove_ids.append(id)
                        elif object_type == 'free_sightseeing':
                            st = Sightseeing.objects.get(id=id)
                            if st.city in cities:
                                object_list.append(st)
                                free_sightseeing_qs_remove_ids.append(id)
                itinerary_objects_list.append(object_list)

            transfer_choices_qs = QuoteTransferInfo.objects.filter(quote=initial_quote).exclude(id__in=transfer_qs_remove_ids)
            sightseeing_choices_qs = QuoteSightseeingInfo.objects.filter(quote=initial_quote).exclude(id__in=sightseeing_qs_remove_ids)
            free_transfer_choices_qs = Transfer.objects.filter(city__in=cities,price=0).exclude(id__in=free_transfer_qs_remove_ids)
            free_sightseeing_choices_qs = Sightseeing.objects.filter(city__in=cities,adult_price=0,child_price=0).exclude(id__in=free_sightseeing_qs_remove_ids)
            itinerary_choices_objects_list = list(transfer_choices_qs) + list(sightseeing_choices_qs) + list(free_transfer_choices_qs) + list(free_sightseeing_choices_qs)
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

        if initial_quote and itinerary_formset.is_valid(): # GETS THE ITINERARY ORDERING TO CONVERT THEM IN OBJECTS LIST FOR VIEW, IF THERE IS ERROR IN SAVING.
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
            hotel_formset.save()
            transfer_formset.save()
            sightseeing_formset.save()
            visa_formset.save()
            insurance_formset.save()
            others_formset.save()
            itinerary_formset.save()

            # CALCULATING PRICE
            pricing_qs_list = (list(quote.quoteflightinfo_set.all()) + list(quote.quotetransportinfo_set.all()) + list(quote.quotehotelinfo_set.all())
                                + list(quote.quotetransferinfo_set.all()) + list(quote.quotesightseeinginfo_set.all()) + list(quote.quotevisainfo_set.all())
                                + list(quote.quoteinsuranceinfo_set.all()) + list(quote.quoteothersinfo_set.all()) )
            quote.price = 0
            for object in pricing_qs_list:
                if object.price:
                    quote.price += object.price
            quote.price = quote.price + quote.mark_up if quote.mark_up else quote.price
            quote.price = quote.price - quote.discount if quote.discount else quote.price
            quote.save()


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

class CustomItineraryView(FormView):
    template_name = 'SalesApp/custom_itinerary_form.html'

    def create_itinerary_lists(self,ordering_list=None):
        initial_quote = self.quote
        itinerary_objects_list = []
        itinerary_choices_objects_list = []
        cities = initial_quote.cities.all()
        trip_duration = (initial_quote.end_date - initial_quote.start_date).days + 1
        current_itinerary_set = initial_quote.quoteitineraryinfo_set.all().order_by('date')

        if not current_itinerary_set:
            date = initial_quote.start_date
            for i in range(trip_duration):
                QuoteItineraryInfo.objects.create(quote=initial_quote,date=date)
                date = date + timedelta(days=1)
                itinerary_objects_list.append([])
            itinerary_choices_objects_list = (list(initial_quote.quotetransferinfo_set.all())
                                                + list(initial_quote.quotesightseeinginfo_set.all())
                                                + list(Transfer.objects.filter(city__in=cities,price=0))
                                                + list(Sightseeing.objects.filter(city__in=cities,adult_price=0,child_price=0))
                                                + list(initial_quote.quoteothersinfo_set.filter(type__in=['TRANSFER','SIGHTSEEING'])))
        else:
            transfer_qs_remove_ids = []
            sightseeing_qs_remove_ids = []
            free_transfer_qs_remove_ids = []
            free_sightseeing_qs_remove_ids = []
            others_qs_remove_ids = []
            if ordering_list is None:
                ordering_list = []
                for object in current_itinerary_set:
                    ordering_list.append(object.ordering)

            current_days = current_itinerary_set.count()
            extra_days = trip_duration - current_days
            previous_start_date = current_itinerary_set.first().date

            if previous_start_date != initial_quote.start_date: # CHECKS IF THE START DATE HAS CHANGED
                for object in current_itinerary_set:
                    QuoteItineraryInfo.objects.update(date=date)
                    date = date + timedelta(days=1)

            if extra_days > 0: # CHECKS IF THE TRIP DURATION HAS CHANGED
                date = initial_quote.start_date + timedelta(days=current_days)
                for i in range(extra_days):
                    QuoteItineraryInfo.objects.create(quote=initial_quote,date=date)
                    date = date + timedelta(days=1)
            elif extra_days < 0:
                delete_qs = QuoteItineraryInfo.objects.filter(date__gt=initial_quote.end_date)
                n = delete_qs.delete()[0] # queryset delete will give the no. of entries deleted
                ordering_list = ordering_list[0:trip_duration]

            for ordering in ordering_list:
                items = ordering.split(',')
                object_list = []
                for item in items:
                    if item:
                        [object_type,id] = item.split('-')
                        if object_type == 'transfer':
                            try: # THIS WILL CHECK IF THE QUOTE-ITINERARY OBJECT HAS BEEN DELETED, OTHERWISE ADD IT TO DISPLAY LIST
                                object_list.append(QuoteTransferInfo.objects.get(id=id))
                                transfer_qs_remove_ids.append(id)
                            except:
                                pass
                        elif object_type == 'sightseeing':
                            try: # THIS WILL CHECK IF THE QUOTE-SIGHTSEEING OBJECT HAS BEEN DELETED, OTHERWISE ADD IT TO DISPLAY LIST
                                object_list.append(QuoteSightseeingInfo.objects.get(id=id))
                                sightseeing_qs_remove_ids.append(id)
                            except:
                                pass
                        elif object_type == 'others':
                            try: # THIS WILL CHECK IF THE QUOTE-OTHERS OBJECT HAS BEEN DELETED, OTHERWISE ADD IT TO DISPLAY LIST
                                object_list.append(QuoteOthersInfo.objects.get(id=id))
                                others_qs_remove_ids.append(id)
                            except:
                                pass
                        elif object_type == 'free_transfer':
                            tr = Transfer.objects.get(id=id)
                            if tr.city in cities:
                                object_list.append(tr)
                                free_transfer_qs_remove_ids.append(id)
                        elif object_type == 'free_sightseeing':
                            st = Sightseeing.objects.get(id=id)
                            if st.city in cities:
                                object_list.append(st)
                                free_sightseeing_qs_remove_ids.append(id)
                itinerary_objects_list.append(object_list)


            transfer_choices_qs = QuoteTransferInfo.objects.filter(quote=initial_quote).exclude(id__in=transfer_qs_remove_ids)
            sightseeing_choices_qs = QuoteSightseeingInfo.objects.filter(quote=initial_quote).exclude(id__in=sightseeing_qs_remove_ids)
            free_transfer_choices_qs = Transfer.objects.filter(city__in=cities,price=0).exclude(id__in=free_transfer_qs_remove_ids)
            free_sightseeing_choices_qs = Sightseeing.objects.filter(city__in=cities,adult_price=0,child_price=0).exclude(id__in=free_sightseeing_qs_remove_ids)
            others_choices_qs = QuoteOthersInfo.objects.filter(quote=initial_quote).filter(type__in=['TRANSFER','SIGHTSEEING']).exclude(id__in=others_qs_remove_ids)
            itinerary_choices_objects_list = list(transfer_choices_qs) + list(sightseeing_choices_qs) + list(free_transfer_choices_qs) + list(free_sightseeing_choices_qs) + list(others_choices_qs)
        return itinerary_objects_list,itinerary_choices_objects_list

    def setup(self, request, *args, **kwargs):
        """Initialize attributes shared by all view methods."""
        self.request = request
        self.args = args
        self.kwargs = kwargs
        self.quote_id = self.request.GET.get('quote_id')
        self.quote = Quote.objects.get(id=self.quote_id)

    def get(self, request, *args, **kwargs):
        """ Handles GET requests and instantiates blank versions of the formsets. """
        form = []
        initial = [{'quote':self.quote}]
        itinerary_formset = QuoteItineraryInfoFormSet(queryset=QuoteItineraryInfo.objects.filter(quote=self.quote),prefix='itinerary')
        itinerary_objects_list,itinerary_choices_objects_list = self.create_itinerary_lists()
        return self.render_to_response(self.get_context_data(form=form, itinerary_formset=itinerary_formset,itinerary_objects_list=itinerary_objects_list,
                                                                itinerary_choices_objects_list=itinerary_choices_objects_list))

    def post(self, request, *args, **kwargs):
        """
        Handles POST requests, instantiating a form instance and its formsets with the passed POST variables and then checking them for validity.
        """
        initial = [{'quote':self.quote}]
        itinerary_formset = QuoteItineraryInfoFormSet(self.request.POST,prefix='itinerary',initial=initial)

        # GET THE ITINERARY ORDERING TO CONVERT THEM IN OBJECTS LIST FOR VIEW, IF THERE IS ERROR IN SAVING.
        ordering_list = []
        for form in itinerary_formset:
            ordering_list.append(form['ordering'].value())
        if (itinerary_formset.is_valid()):
            return self.form_valid(itinerary_formset)
        else:
            itinerary_objects_list,itinerary_choices_objects_list = self.create_itinerary_lists(ordering_list=ordering_list)
            return self.form_invalid(itinerary_formset,itinerary_objects_list,itinerary_choices_objects_list)

    def form_valid(self,itinerary_formset):
        """ Called if all forms are valid. Saves all formsets, updates quote boolean flags and then redirects to a success page. """
        itinerary_formset.save()
        self.quote.quote_itinerary = True
        if self.quote.inclusions_updated:
            self.quote.itinerary_updated = True
            self.quote.quote_valid = True
        self.quote.save()
        return HttpResponseRedirect(reverse('SalesApp:quote_detail', args=[self.quote.id]))

    def form_invalid(self,itinerary_formset,itinerary_objects_list,itinerary_choices_objects_list):
        """ Called if a form is invalid. Re-renders the context data with the data-filled forms and errors. """
        form = []
        return self.render_to_response(self.get_context_data(form=form, itinerary_formset=itinerary_formset,
                                                                        itinerary_objects_list=itinerary_objects_list,
                                                                        itinerary_choices_objects_list=itinerary_choices_objects_list))



class CustomInclusionsView(FormView):
    template_name = 'SalesApp/custom_inclusions_form.html'

    def setup(self, request, *args, **kwargs):
        """Initialize attributes shared by all view methods."""
        self.request = request
        self.args = args
        self.kwargs = kwargs
        self.quote_id = self.request.GET.get('quote_id')
        self.quote = Quote.objects.get(id=self.quote_id)

    def get(self, request, *args, **kwargs):
        """
        Handles GET requests and instantiates blank versions of the formsets.
        """
        form = []
        initial = [{'quote':self.quote}]
        flight_formset = QuoteFlightInfoFormSet(queryset=QuoteFlightInfo.objects.filter(quote__id=self.quote_id),initial=initial,prefix='flight')
        transport_formset = QuoteTransportInfoFormSet(queryset=QuoteTransportInfo.objects.filter(quote__id=self.quote_id),initial=initial,prefix='transport')
        hotel_formset = QuoteHotelInfoFormSet(queryset=QuoteHotelInfo.objects.filter(quote__id=self.quote_id),initial=initial,prefix='hotel')
        transfer_formset = QuoteTransferInfoFormSet(queryset=QuoteTransferInfo.objects.filter(quote__id=self.quote_id),initial=initial,prefix='transfer')
        sightseeing_formset = QuoteSightseeingInfoFormSet(queryset=QuoteSightseeingInfo.objects.filter(quote__id=self.quote_id),initial=initial,prefix='sightseeing')
        visa_formset = QuoteVisaInfoFormSet(queryset=QuoteVisaInfo.objects.filter(quote__id=self.quote_id),initial=initial,prefix='visa')
        insurance_formset = QuoteInsuranceInfoFormSet(queryset=QuoteInsuranceInfo.objects.filter(quote__id=self.quote_id),initial=initial,prefix='insurance')
        others_formset = QuoteOthersInfoFormSet(queryset=QuoteOthersInfo.objects.filter(quote__id=self.quote_id),initial=initial,prefix='others')
        return self.render_to_response(self.get_context_data(form=form, flight_formset=flight_formset,
                                                                        transport_formset=transport_formset,
                                                                        hotel_formset=hotel_formset,
                                                                        transfer_formset=transfer_formset,
                                                                        sightseeing_formset=sightseeing_formset,
                                                                        visa_formset=visa_formset,
                                                                        insurance_formset=insurance_formset,
                                                                        others_formset=others_formset))

    def post(self, request, *args, **kwargs):
        """
        Handles POST requests, instantiating a form instance and its formsets with the passed POST variables and then checking them for validity.
        """
        initial = [{'quote':self.quote}]
        flight_formset = QuoteFlightInfoFormSet(request.POST,prefix='flight',initial=initial)
        transport_formset = QuoteTransportInfoFormSet(request.POST,prefix='transport',initial=initial)
        hotel_formset = QuoteHotelInfoFormSet(request.POST,prefix='hotel',initial=initial)
        transfer_formset = QuoteTransferInfoFormSet(request.POST,prefix='transfer',initial=initial)
        sightseeing_formset = QuoteSightseeingInfoFormSet(request.POST,prefix='sightseeing',initial=initial)
        visa_formset = QuoteVisaInfoFormSet(request.POST,prefix='visa',initial=initial)
        insurance_formset = QuoteInsuranceInfoFormSet(request.POST,prefix='insurance',initial=initial)
        others_formset = QuoteOthersInfoFormSet(request.POST,prefix='others',initial=initial)

        if (flight_formset.is_valid() and transport_formset.is_valid() and hotel_formset.is_valid() and
            transfer_formset.is_valid() and sightseeing_formset.is_valid() and visa_formset.is_valid() and
            insurance_formset.is_valid() and others_formset.is_valid()):

            return self.form_valid(flight_formset,transport_formset,hotel_formset,transfer_formset,sightseeing_formset,visa_formset,insurance_formset,others_formset)
        else:
            return self.form_invalid(flight_formset,transport_formset,hotel_formset,transfer_formset,sightseeing_formset,visa_formset,insurance_formset,others_formset)

    def form_valid(self,flight_formset,transport_formset,hotel_formset,transfer_formset,sightseeing_formset,visa_formset,insurance_formset,others_formset):
        """
        Called if all forms are valid. Saves all formsets, updates quote boolean flags and then redirects to a success page.
        """
        flight_formset.save()
        transport_formset.save()
        hotel_formset.save()
        transfer_formset.save()
        sightseeing_formset.save()
        visa_formset.save()
        insurance_formset.save()
        others_formset.save()

        self.quote.quote_inclusions = True
        self.quote.inclusions_updated = True
        self.quote.inclusions_format = 'CUSTOM'
        self.quote.itinerary_updated = False
        self.quote.quote_valid = False
        self.quote.save()
        return HttpResponseRedirect(reverse('SalesApp:quote_detail', args=[self.quote.id]))

    def form_invalid(self,flight_formset,transport_formset,hotel_formset,transfer_formset,sightseeing_formset,visa_formset,insurance_formset,others_formset):
        """
        Called if a form is invalid. Re-renders the context data with the data-filled forms and errors.
        """
        form = []
        return self.render_to_response(self.get_context_data(form=form, flight_formset=flight_formset,
                                                                        transport_formset=transport_formset,
                                                                        hotel_formset=hotel_formset,
                                                                        transfer_formset=transfer_formset,
                                                                        sightseeing_formset=sightseeing_formset,
                                                                        visa_formset=visa_formset,
                                                                        insurance_formset=insurance_formset,
                                                                        others_formset=others_formset))


class FlexInclusionsCreateView(CreateView):
    model = FlexInclusions
    form_class = FlexInclusionsForm

    def get_initial(self):
        initial = super().get_initial()
        quote_id = self.request.GET.get("quote_id")
        initial['quote'] = Quote.objects.get(id=quote_id)
        return initial

class FlexInclusionsUpdateView(UpdateView):
    model = FlexInclusions
    form_class = FlexInclusionsForm

    def get_object(self):
        pk = self.request.GET.get('quote_id')
        return FlexInclusions.objects.get(quote__id=pk)

class FlexItineraryCreateView(CreateView):
    model = FlexItinerary
    form_class = FlexItineraryForm

    def get_initial(self):
        initial = super().get_initial()
        quote_id = self.request.GET.get("quote_id")
        initial['quote'] = Quote.objects.get(id=quote_id)
        return initial

class FlexItineraryUpdateView(UpdateView):
    model = FlexItinerary
    form_class = FlexItineraryForm

    def get_object(self):
        pk = self.request.GET.get('quote_id')
        return FlexItinerary.objects.get(quote__id=pk)

class QuoteCreateView(CreateView):
    model = Quote
    form_class = QuoteForm

    def get_initial(self):
        """  Returns the initial data to use for forms on this view. """
        initial = super().get_initial()
        try:
            lead_id = self.request.GET.get("lead_id")
            lead = Lead.objects.get(id=lead_id)
            initial['lead'] = lead
            initial['destinations'] = lead.destinations.all()
        except:
            pass
        return initial

class QuoteUpdateView(UpdateView):
    model = Quote
    form_class = QuoteForm

class QuoteDetailView(DetailView):
    model = Quote
