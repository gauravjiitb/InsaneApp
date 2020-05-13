import time
from datetime import timedelta,date
import json, itertools
from decimal import Decimal

from django.shortcuts import render, HttpResponseRedirect
from django.contrib.auth.mixins import LoginRequiredMixin,UserPassesTestMixin
from django.views.generic import TemplateView,ListView,DetailView,CreateView,UpdateView,FormView
from django.urls import reverse_lazy,reverse
from django.db.models import F,Q

from django_filters.views import FilterView
from extra_views import InlineFormSetView

from SalesApp.models import Lead,Quote, Package, Inclusion, FlexInclusions,FlexItinerary, HotelGroup
from ProfilesApp.models import Customer
from OperationsApp.models import Booking
from ContentApp.models import Destination,City,Transport,Hotel,Transfer,Sightseeing,Visa,Insurance, Pricing
from SalesApp.filters import LeadFilter, PackageFilter, QuoteFilter
from SalesApp.forms import (LeadForm, QuoteForm, FlexInclusionsForm, FlexItineraryForm, PackageForm, HotelGroupFS,
                                PackageInclusionFormSet, ItineraryFormSet, QuoteInclusionFormSet,HotelGroupForm,QuotePackagesSelectForm)
from ContentApp.forms import PackagePricingFS, InclusionPricingFS



################################################################################
# UTILITY FUNCTIONS
################################################################################

def quote_load_cities(request):
    template_name = 'SalesApp/ajax/city_dropdown_list_options.html'
    destination_ids = request.GET.getlist('destinations[]')
    destinations = Destination.objects.filter(pk__in=destination_ids)
    cities = City.objects.filter(destination__in=destinations).order_by('name')
    return render(request, template_name, {'cities': cities})

def quote_load_hotels(request):
    city_id = request.GET.get('city_id')
    hotels = Hotel.objects.filter(city__id=city_id).order_by('name')
    return render(request, 'SalesApp/ajax/hotels_dropdown_options.html', {'hotels': hotels})

def quote_load_transfers(request):
    city_id = request.GET.get('city_id')
    transfers = Transfer.objects.filter(city__id=city_id)
    return render(request, 'SalesApp/ajax/transfers_dropdown_options.html', {'transfers': transfers})

def quote_load_sightseeings(request):
    city_id = request.GET.get('city_id')
    sightseeings = Sightseeing.objects.filter(city__id=city_id)
    return render(request, 'SalesApp/ajax/sightseeings_dropdown_options.html', {'sightseeings': sightseeings})

def quote_load_transports(request):
    city_id = request.GET.get('city_id')
    sightseeings = Sightseeing.objects.filter(city__id=city_id)
    return render(request, 'SalesApp/ajax/sightseeings_dropdown_options.html', {'sightseeings': sightseeings})

def package_load_hotelgroups(request):
    package_id = request.GET.get('package_id')
    package = Package.objects.get(id=package_id)
    hotel_groups = package.hotelgroup_set.all()
    return render(request, 'SalesApp/ajax/hotelgroups_options.html', {'hotel_groups':hotel_groups})

################################################################################




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
        context['bookings'] = Booking.objects.filter(quote__lead = primary_key)
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
#   PACKAGE VIEWS
###############################

class PackageCreateView(LoginRequiredMixin,CreateView):
    form_class = PackageForm
    model = Package

class PackageListView(LoginRequiredMixin,FilterView):
        template_name = 'SalesApp/package_list.html'
        paginate_by = 10
        form_class = PackageForm
        filterset_class = PackageFilter
        ordering = ['id']

class PackageDetailView(LoginRequiredMixin,DetailView):
    model = Package
    def get_context_data(self,**kwargs):
        context = super(PackageDetailView,self).get_context_data(**kwargs)
        pk = self.kwargs.get('pk')
        package = Package.objects.get(id=pk)
        hotel_groups = []
        for group in package.hotelgroup_set.all():
            hotel_groups.append(list(group.inclusion_set.all()))
        context['hotel_groups'] = hotel_groups
        if package.package_inclusions:
            objects_list = []
            optionals_list = []
            for inclusion in package.inclusion_set.all():
                if inclusion.item_type == 'TRANSFER':
                    objects_list += list(inclusion.transfers.all())
                elif inclusion.item_type == 'SIGHTSEEING':
                    objects_list += list(inclusion.sightseeings.all())
                elif inclusion.item_type == 'TRANSPORT':
                    objects_list += list(inclusion.transports.all())
                elif inclusion.item_type == 'VISA':
                    objects_list += list(inclusion.visas.all())
                elif inclusion.item_type == 'INSURANCE':
                    objects_list.append(inclusion.insurance)
                else:
                    objects_list.append(inclusion)

                if inclusion.optional:
                    optionals_list.append(inclusion)
            context['inclusions'] = objects_list
            context['optionals_list'] = optionals_list
        if package.package_itinerary:
            itinerary_objects_list = []
            include_list = json.loads(package.itinerary)
            for day in include_list:
                object_list = []
                for item in day:
                    if item:
                        [object_type,id] = item.split('-')
                        if object_type == 'transfer':
                            object_list.append(Transfer.objects.get(id=id))
                        elif object_type == 'sightseeing':
                            object_list.append(Sightseeing.objects.get(id=id))
                        elif object_type == 'transport':
                            object_list.append(Transport.objects.get(id=id))
                        elif object_type == 'other':
                            object_list.append(Inclusion.objects.get(id=id))
                itinerary_objects_list.append(object_list)
            context['itinerary_objects_list'] = itinerary_objects_list
        context['pricing_list'] = list(package.pricing_set.all())
        return context


class PackageUpdateView(LoginRequiredMixin,UpdateView):
    form_class = PackageForm
    model = Package

class HotelGroupCreateView(CreateView):
    model = HotelGroup
    fields = ['package','name']
    def get_initial(self):
        initial = super().get_initial()
        pk = self.kwargs['pk']
        initial['package'] = Package.objects.get(id=pk)
        return initial
    def get_success_url(self):
        return reverse('SalesApp:package_hotels_create', kwargs={'pk': self.object.id})


class PackageHotelsCreateView(InlineFormSetView):
    template_name = 'SalesApp/hotel_group_options_form.html'
    model = HotelGroup
    inline_model = Inclusion
    # fields = ['item_type','nights','hotel','room_type']
    form_class = HotelGroupForm
    formset_class = HotelGroupFS
    initial = [{'item_type': 'HOTEL'},{'item_type': 'HOTEL'},{'item_type': 'HOTEL'}]
    factory_kwargs = {'extra': 3, 'can_delete': True}
    def get_success_url(self):
        return reverse('SalesApp:package_detail', kwargs={'pk': self.object.package.id})

class PackageInclusionView(FormView):
    template_name = 'SalesApp/package_inclusion_form.html'

    def setup(self, request, *args, **kwargs):
        """Initialize attributes shared by all view methods."""
        self.request = request
        self.args = args
        self.kwargs = kwargs
        self.package_id = self.kwargs['pk']
        self.package = Package.objects.get(id=self.package_id)

    def get(self, request, *args, **kwargs):
        form = []
        inclusion_formset = PackageInclusionFormSet(instance=self.package,queryset=self.package.inclusion_set.order_by("display_order"))
        return self.render_to_response(self.get_context_data(form=form, inclusion_formset=inclusion_formset, package=self.package))

    def post(self, request, *args, **kwargs):
        form = []
        inclusion_formset = PackageInclusionFormSet(self.request.POST,instance=self.package)
        if inclusion_formset.is_valid():
            inclusion_formset.save()
            self.package.package_inclusions = True
            self.package.inclusions_updated = True
            self.package.itinerary_updated = False
            self.package.package_valid = False
            self.package.save()
            return HttpResponseRedirect(reverse('SalesApp:package_detail', args=[self.package_id]))
        else:
            return self.render_to_response(self.get_context_data(form=form, inclusion_formset=inclusion_formset, package=self.package))

class PackageItineraryView(FormView):
    template_name = 'SalesApp/itinerary_form.html'

    def load_itinerary_lists(self):
        package = self.package
        itinerary_objects_list = []
        itinerary_choices_objects_list = []

        for inclusion in package.inclusion_set.all():
            if inclusion.item_type == 'TRANSFER':
                itinerary_choices_objects_list += list(inclusion.transfers.all())
            elif inclusion.item_type == 'SIGHTSEEING':
                itinerary_choices_objects_list += list(inclusion.sightseeings.all())
            elif inclusion.item_type == 'TRANSPORT':
                itinerary_choices_objects_list += list(inclusion.transports.exclude(description__exact=''))
            elif inclusion.item_type == 'OTHER' and inclusion.other_type in ['TRANSPORT','TRANSFER','SIGHTSEEING']:
                itinerary_choices_objects_list.append(inclusion)
        if self.itinerary:
            if len(self.itinerary) > package.duration:
                include_list =  self.itinerary[:package.duration]
            else:
                include_list = self.itinerary

            for day in include_list:
                object_list = []
                for item in day:
                    if item:
                        [object_type,id] = item.split('-')
                        if object_type == 'transfer':
                            tr = Transfer.objects.get(id=id)
                            # CHECK IF THE QUOTE-ITINERARY OBJECT HAS BEEN DELETED, OTHERWISE ADD IT TO DISPLAY LIST
                            if tr in itinerary_choices_objects_list:
                                object_list.append(tr)
                                itinerary_choices_objects_list.remove(tr)
                        elif object_type == 'sightseeing':
                            sg = Sightseeing.objects.get(id=id)
                            if sg in itinerary_choices_objects_list:
                                object_list.append(sg)
                                itinerary_choices_objects_list.remove(sg)
                        elif object_type == 'transport':
                            tp = Transport.objects.get(id=id)
                            if tp in itinerary_choices_objects_list:
                                object_list.append(tp)
                                itinerary_choices_objects_list.remove(tp)
                        elif object_type == 'other':
                            try: # CHECK IF THIS OBJECT HAS BEEN DELETED, OTHERWISE ADD IT TO DISPLAY LIST
                                ot = Inclusion.objects.get(id=id)
                                object_list.append(ot)
                                itinerary_choices_objects_list.remove(ot)
                            except:
                                pass
                itinerary_objects_list.append(object_list)
            if package.duration > len(include_list):
                for i in range(package.duration - len(include_list)):
                    itinerary_objects_list.append([])
        else:
            for i in range(package.duration):
                itinerary_objects_list.append([])
        return itinerary_objects_list,itinerary_choices_objects_list


    def setup(self, request, *args, **kwargs):
        # ITINERARY FORMAT-- [[transport-45,transfer-6,sightseeing-31],[sightseeing-56,transfer-12,..],[],...]
        self.request = request
        self.args = args
        self.kwargs = kwargs
        self.package_id = self.kwargs['pk']
        self.package = Package.objects.get(id=self.package_id)
        if self.package.itinerary:
            self.itinerary = json.loads(self.package.itinerary)
        else:
            self.itinerary = ''
        self.initial = []
        for i in range(self.package.duration):
            self.initial.append([])


    def get(self, request, *args, **kwargs):
        form = []
        itinerary_objects_list,itinerary_choices_objects_list = self.load_itinerary_lists()
        itinerary_formset = ItineraryFormSet(initial=self.initial)
        return self.render_to_response(self.get_context_data(form=form, itinerary_formset=itinerary_formset,itinerary_objects_list=itinerary_objects_list,
                                                                    itinerary_choices_objects_list=itinerary_choices_objects_list))

    def post(self, request, *args, **kwargs):
        form = []
        itinerary_formset = ItineraryFormSet(request.POST,initial=self.initial)
        itinerary_list = []
        # ITINERARY FORMAT-- [[transport-45,transfer-6,sightseeing-31],[sightseeing-56,transfer-12,..],[],...]
        if itinerary_formset.is_valid():
            for form in itinerary_formset:
                itinerary = form.cleaned_data.get('itinerary')
                if itinerary:
                    itinerary_list.append(itinerary.split(','))
                else:
                    itinerary_list.append([])
            self.package.itinerary = json.dumps(itinerary_list)
            self.package.package_itinerary = True
            if self.package.inclusions_updated:
                self.package.itinerary_updated = True
                self.package.package_valid = True
            self.package.save()
            return HttpResponseRedirect(reverse('SalesApp:package_detail', args=[self.package_id]))
        else:
            return self.render_to_response(self.get_context_data(form=form, itinerary_formset=itinerary_formset,itinerary_objects_list=itinerary_objects_list,
                                                                        itinerary_choices_objects_list=itinerary_choices_objects_list))

class PackagePricingView(FormView):
    template_name = 'SalesApp/pricing_form.html'
    def setup(self, request, *args, **kwargs):
        """Initialize attributes shared by all view methods."""
        self.request = request
        self.args = args
        self.package_id = kwargs['pk']
        self.package = Package.objects.get(id=self.package_id)
    def get(self, request, *args, **kwargs):
        form = []
        formset = PackagePricingFS(instance=self.package)
        return self.render_to_response(self.get_context_data(form=form, formset=formset,package_id=self.package_id))
    def post(self, request, *args, **kwargs):
        form = []
        formset = PackagePricingFS(self.request.POST,instance=self.package)
        if formset.is_valid():
            formset.save()
            # return HttpResponseRedirect(reverse('SalesApp:package_detail', args=[self.package_id]))
        else:
            return self.render_to_response(self.get_context_data(form=form, formset=formset, package_id=self.package_id))

class PackageOptionalsPricingView(FormView):
    template_name = 'SalesApp/pricing_form.html'

    def setup(self, request, *args, **kwargs):
        self.request = request
        self.args = args
        self.inclusion = Inclusion.objects.get(id=kwargs['pk'])

    def get(self, request, *args, **kwargs):
        form = []
        formset = InclusionPricingFS(instance=self.inclusion)
        return self.render_to_response(self.get_context_data(form=form, formset=formset))

    def post(self, request, *args, **kwargs):
        form = []
        formset = InclusionPricingFS(self.request.POST,instance=self.inclusion)
        if formset.is_valid():
            formset.save()
        else:
            print(formset.errors)
            return self.render_to_response(self.get_context_data(form=form, formset=formset))

###############################
#   QUOTE VIEWS
###############################

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
    def get_context_data(self,**kwargs):
        context = super(QuoteUpdateView,self).get_context_data(**kwargs)
        pk = self.kwargs.get('pk')
        quote = Quote.objects.get(id=pk)
        inclusions_pricing_list, context['auto_price'] = quote.get_quote_price_list()
        return context
    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        if self.object.booked:
            return HttpResponseRedirect(reverse('error403'))
        else:
            return super().get(request, *args, **kwargs)

class QuoteDetailView(DetailView):
    model = Quote
    def get_context_data(self,**kwargs):
        context = super(QuoteDetailView,self).get_context_data(**kwargs)
        pk = self.kwargs.get('pk')
        quote = Quote.objects.get(id=pk)
        # context['inclusions'] = quote.get_included_objects()
        context['inclusions_pricing_list'], context['auto_price'] = quote.get_quote_price_list()
        context['itinerary_objects_list'] = quote.get_daywise_itinerary_objects()
        quote.refresh_from_db()
        context['quote'] = quote
        return context

class QuoteListView(LoginRequiredMixin,FilterView):
        template_name = 'SalesApp/quote_list.html'
        paginate_by = 10
        form_class = QuoteForm
        filterset_class = QuoteFilter
        ordering = ['id']

class QuoteItineraryView(FormView):
    template_name = 'SalesApp/itinerary_form.html'

    def load_itinerary_lists(self):
        quote = self.quote
        itinerary_objects_list = []
        itinerary_choices_objects_list = []

        for inclusion in quote.inclusion_set.all():
            if inclusion.item_type == 'TRANSFER':
                itinerary_choices_objects_list += list(inclusion.transfers.all())
            elif inclusion.item_type == 'SIGHTSEEING':
                itinerary_choices_objects_list += list(inclusion.sightseeings.all())
            elif inclusion.item_type == 'TRANSPORT':
                itinerary_choices_objects_list += list(inclusion.transports.exclude(description__exact=''))
            elif inclusion.item_type == 'VARIABLE_TRANSPORT' and inclusion.variable_transports.description != '':
                itinerary_choices_objects_list.append(inclusion.variable_transports)
            elif inclusion.item_type == 'OTHER' and inclusion.other_type in ['TRANSPORT','TRANSFER','SIGHTSEEING']:
                itinerary_choices_objects_list.append(inclusion)
        if self.itinerary:
            if len(self.itinerary) > self.duration:
                include_list =  self.itinerary[:self.duration]
            else:
                include_list = self.itinerary

            for day in include_list:
                object_list = []
                for item in day:
                    if item:
                        [object_type,id] = item.split('-')
                        if object_type == 'transfer':
                            tr = Transfer.objects.get(id=id)
                            # CHECK IF THE OBJECT HAS BEEN DELETED, OTHERWISE ADD IT TO DISPLAY LIST
                            if tr in itinerary_choices_objects_list:
                                object_list.append(tr)
                                itinerary_choices_objects_list.remove(tr)
                        elif object_type == 'sightseeing':
                            sg = Sightseeing.objects.get(id=id)
                            if sg in itinerary_choices_objects_list:
                                object_list.append(sg)
                                itinerary_choices_objects_list.remove(sg)
                        elif object_type == 'transport':
                            tp = Transport.objects.get(id=id)
                            if tp in itinerary_choices_objects_list:
                                object_list.append(tp)
                                itinerary_choices_objects_list.remove(tp)
                        elif object_type == 'other':
                            try: # CHECK IF THIS OBJECT HAS BEEN DELETED, OTHERWISE ADD IT TO DISPLAY LIST
                                ot = Inclusion.objects.get(id=id)
                                object_list.append(ot)
                                itinerary_choices_objects_list.remove(ot)
                            except:
                                pass
                itinerary_objects_list.append(object_list)
            if self.duration > len(include_list):
                for i in range(self.duration - len(include_list)):
                    itinerary_objects_list.append([])
        else:
            for i in range(self.duration):
                itinerary_objects_list.append([])
        return itinerary_objects_list,itinerary_choices_objects_list

    def setup(self, request, *args, **kwargs):
        # ITINERARY FORMAT-- [[transport-45,transfer-6,sightseeing-31],[sightseeing-56,transfer-12,..],[],...]
        self.request = request
        self.args = args
        self.kwargs = kwargs
        self.quote_id = self.kwargs['pk']
        self.quote = Quote.objects.get(id=self.quote_id)
        self.duration = (self.quote.end_date - self.quote.start_date).days + 1
        if self.quote.itinerary:
            self.itinerary = json.loads(self.quote.itinerary)
        else:
            self.itinerary = ''
        self.initial = []
        for i in range(self.duration):
            self.initial.append([])

    def get(self, request, *args, **kwargs):
        form = []
        if not self.quote.booked:
            itinerary_objects_list,itinerary_choices_objects_list = self.load_itinerary_lists()
            itinerary_formset = ItineraryFormSet(initial=self.initial)
            return self.render_to_response(self.get_context_data(form=form, itinerary_formset=itinerary_formset,itinerary_objects_list=itinerary_objects_list,
                                                                        itinerary_choices_objects_list=itinerary_choices_objects_list))
        else:
            return HttpResponseRedirect(reverse('error403'))

    def post(self, request, *args, **kwargs):
        form = []
        itinerary_formset = ItineraryFormSet(request.POST,initial=self.initial)
        itinerary_list = []
        # ITINERARY FORMAT-- [[transport-45,transfer-6,sightseeing-31],[sightseeing-56,transfer-12,..],[],...]
        if itinerary_formset.is_valid():
            for form in itinerary_formset:
                itinerary = form.cleaned_data.get('itinerary')
                if itinerary:
                    itinerary_list.append(itinerary.split(','))
                else:
                    itinerary_list.append([])
            self.quote.itinerary = json.dumps(itinerary_list)
            self.quote.quote_itinerary = True
            if self.quote.inclusions_updated:
                self.quote.itinerary_updated = True
                self.quote.quote_valid = True
            self.quote.save()
            return HttpResponseRedirect(reverse('SalesApp:quote_detail', args=[self.quote_id]))
        else:
            return self.render_to_response(self.get_context_data(form=form, itinerary_formset=itinerary_formset,itinerary_objects_list=itinerary_objects_list,
                                                                        itinerary_choices_objects_list=itinerary_choices_objects_list))

class QuoteInclusionView(FormView):
    template_name = 'SalesApp/quote_inclusion_form.html'

    def setup(self, request, *args, **kwargs):
        """Initialize attributes shared by all view methods."""
        self.request = request
        self.args = args
        self.kwargs = kwargs
        self.quote_id = self.kwargs['pk']
        self.quote = Quote.objects.get(id=self.quote_id)

    def get(self, request, *args, **kwargs):
        form = []
        if not self.quote.booked:
            inclusion_formset = QuoteInclusionFormSet(instance=self.quote,queryset=self.quote.inclusion_set.order_by("display_order"))
            return self.render_to_response(self.get_context_data(form=form, inclusion_formset=inclusion_formset))
        else:
            return HttpResponseRedirect(reverse('error403'))

    def post(self, request, *args, **kwargs):
        form = []
        inclusion_formset = QuoteInclusionFormSet(self.request.POST,instance=self.quote)
        if inclusion_formset.is_valid():
            inclusion_formset.save()
            self.quote.quote_inclusions = True
            self.quote.inclusions_updated = True
            self.quote.itinerary_updated = False
            self.quote.quote_valid = False
            self.quote.save()
            return HttpResponseRedirect(reverse('SalesApp:quote_detail', args=[self.quote_id]))
        else:
            return self.render_to_response(self.get_context_data(form=form, inclusion_formset=inclusion_formset))

def quote_package_selection(request,pk):
    template_name = 'SalesApp/quote_package_selection.html'
    quote = Quote.objects.get(id=pk)
    if request.POST:
        form = QuotePackagesSelectForm(request.POST)
        if form.is_valid():
            quote.inclusion_set.all().delete()
            packages = [form.cleaned_data.get('package1'),form.cleaned_data.get('package2'),form.cleaned_data.get('package3')]
            hotel_groups = [form.cleaned_data.get('hotel_group1'),form.cleaned_data.get('hotel_group2'),form.cleaned_data.get('hotel_group3')]
            print(hotel_groups)
            for package in packages:
                if package:
                    for inclusion in package.inclusion_set.all():
                        if inclusion:
                            if inclusion.item_type in ['TRANSFER','SIGHTSEEING','VISA']:
                                sightseeings = inclusion.sightseeings.all()
                                transfers = inclusion.transfers.all()
                                visas = inclusion.visas.all()
                                inclusion.pk = None
                                inclusion.package = None
                                inclusion.quote = quote
                                inclusion.save()
                                inclusion.sightseeings.set(sightseeings)
                                inclusion.transfers.set(transfers)
                                inclusion.visas.set(visas)
                            elif inclusion.item_type == 'TRANSPORT':
                                transports = inclusion.transports.filter(variable_pricing=False)
                                variable_transports_qs = inclusion.transports.filter(variable_pricing=True)
                                inclusion.pk = None
                                inclusion.package = None
                                inclusion.quote = quote
                                inclusion.save()
                                inclusion.transports.set(transports)
                                for tr in variable_transports_qs:
                                    inclusion.pk = None
                                    inclusion.quote = quote
                                    inclusion.item_type = 'VARIABLE_TRANSPORT'
                                    inclusion.variable_transports = tr
                                    inclusion.save()
                            elif inclusion.item_type == 'INSURANCE':
                                insurance = inclusion.insurance
                                inclusion.pk = None
                                inclusion.package = None
                                inclusion.quote = quote
                                inclusion.insurance = insurance
                                inclusion.save()
                            elif inclusion.item_type in ['FLIGHT','OTHER','EXCLUSION']:
                                inclusion.pk = None
                                inclusion.package = None
                                inclusion.quote = quote
                                inclusion.save()
            for hotel_group in hotel_groups:
                if hotel_group:
                    for inclusion in hotel_group.inclusion_set.all():
                        if inclusion:
                            inclusion.pk = None
                            inclusion.hotel_group = None
                            inclusion.quote = quote
                            inclusion.save()

            quote.inclusions_format = 'CUSTOM'
            quote.quote_inclusions = True
            quote.save()
            return HttpResponseRedirect(reverse('SalesApp:quote_detail', kwargs={'pk':quote.id}))
    else:
        if not quote.booked:
            form = QuotePackagesSelectForm()
            return render(request, template_name, {'form': form})
        else:
            return HttpResponseRedirect(reverse('error403'))


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
