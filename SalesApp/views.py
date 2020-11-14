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

from SalesApp.models import Lead,Quote, Package, Inclusion, HotelGroup
from ProfilesApp.models import Customer
from OperationsApp.models import Booking
from ContentApp.models import Destination,City,Transport,Hotel,Transfer,Sightseeing,Visa,Insurance, Pricing
from SalesApp.filters import LeadFilter, PackageFilter, QuoteFilter
from SalesApp.forms import (LeadForm, QuoteForm, QuoteInclusionForm, QuoteInclusionFS, HotelGroupForm, HotelGroupFS, QuotePackagesSelectForm,
                            InclusionBulkSelectForm, PackageForm, PackageInclusionForm, PackageInclusionFS)
from ContentApp.forms import PricingForm
from InsaneDjangoApp.mixins import LeadAddPM, LeadEditPM, LeadViewPM



################################################################################
# AJAX VIEWS
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



###############################
#   QUOTE VIEWS
###############################

class QuoteCreateView(CreateView):
    model = Quote
    form_class = QuoteForm
    template_name = 'SalesApp/quote/quote_form.html'

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
    template_name = 'SalesApp/quote/quote_form.html'

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        if self.object.lead.lead_status == 'BOOKED':
            return HttpResponseRedirect(reverse('error403'))
        else:
            return super().get(request, *args, **kwargs)

class QuoteDetailView(DetailView):
    model = Quote
    template_name = 'SalesApp/quote/quote_detail.html'
    def get_context_data(self,**kwargs):
        context = super(QuoteDetailView,self).get_context_data(**kwargs)
        pk = self.kwargs.get('pk')
        quote = Quote.objects.get(id=pk)
        context['inclusions_list'], context['auto_price'] = quote.get_inclusions_price_list()
        context['itinerary'] = quote.get_daywise_itinerary()
        quote.refresh_from_db()
        context['quote'] = quote
        return context

class QuoteListView(LoginRequiredMixin,FilterView):
        template_name = 'SalesApp/quote/quote_list.html'
        paginate_by = 10
        form_class = QuoteForm
        filterset_class = QuoteFilter
        ordering = ['id']

def quote_package_selection(request,pk):
    template_name = 'SalesApp/quote_package_selection.html'
    quote = Quote.objects.get(id=pk)
    if request.POST:
        form = QuotePackagesSelectForm(request.POST)
        if form.is_valid():
            quote.inclusion_set.all().delete()
            packages = [form.cleaned_data.get('package1'),form.cleaned_data.get('package2'),form.cleaned_data.get('package3')]
            hotel_groups = [form.cleaned_data.get('hotel_group1'),form.cleaned_data.get('hotel_group2'),form.cleaned_data.get('hotel_group3')]
            for i,package in enumerate(packages):
                if package:
                    quote.packages.add(package)
                    quote.save()
                    for inclusion in package.inclusion_set.all():
                        if inclusion:
                            inclusion.pk = None
                            inclusion.package = None
                            inclusion.quote = quote

                            if inclusion.day:
                                inclusion.day = inclusion.day + i*package.duration
                            if package.type == 'FIXED':
                                inclusion.fixed_package_item = True
                            inclusion.save()
            for hotel_group in hotel_groups:
                if hotel_group:
                    for inclusion in hotel_group.inclusion_set.all():
                        if inclusion:
                            inclusion.pk = None
                            inclusion.hotel_group = None
                            inclusion.quote = quote
                            if hotel_group.package.type == 'FIXED':
                                inclusion.fixed_package_item = True
                            inclusion.save()

            quote.inclusions_format = 'CUSTOM'
            # quote.inclusions_exist = True
            quote.save()
            return HttpResponseRedirect(reverse('SalesApp:quote_detail', kwargs={'pk':quote.id}))
    else:
        if not quote.booked:
            form = QuotePackagesSelectForm()
            return render(request, template_name, {'form': form})
        else:
            return HttpResponseRedirect(reverse('error403'))

class QuoteInclusionView(InlineFormSetView):
    template_name = 'SalesApp/quote/quote_inclusion_form.html'
    model = Quote
    inline_model = Inclusion
    form_class = QuoteInclusionForm
    formset_class = QuoteInclusionFS
    factory_kwargs = {'extra': 3, 'can_delete': True}

    def get_success_url(self):
        return reverse('SalesApp:quote_detail', kwargs={'pk': self.object.id})
    def get_formset_kwargs(self):
        kwargs = super(QuoteInclusionView, self).get_formset_kwargs()
        kwargs['queryset'] = self.object.inclusion_set.order_by("item_type")
        return kwargs
    def formset_valid(self, formset):
        self.object.inclusions_updated = True
        self.object.inclusions_exist = True
        self.object.itinerary_updated = False
        self.object.price_valid = False
        self.object.quote_valid = False
        self.object.save()
        return super(QuoteInclusionView, self).formset_valid(formset)

class QuoteInclusionBulkSelectView(FormView):
    template_name = 'SalesApp/inclusion_bulk_select.html'

    def setup(self, request, *args, **kwargs):
        self.request = request
        self.args = args
        self.kwargs = kwargs
        self.quote_id = self.kwargs['pk']
        self.quote = Quote.objects.get(id=self.quote_id)

    def get(self, request, *args, **kwargs):
        form = InclusionBulkSelectForm(object=self.quote)
        return self.render_to_response(self.get_context_data(form=form))

    def post(self, request, *args, **kwargs):
        form = InclusionBulkSelectForm(self.request.POST, object=self.quote)
        if form.is_valid():
            for transport in form.cleaned_data.get('transports'):
                Inclusion.objects.create(quote=self.quote, transport=transport, item_type='2_TRANSPORT')
            for transfer in form.cleaned_data.get('transfers'):
                Inclusion.objects.create(quote=self.quote, transfer=transfer, item_type='3_TRANSFER')
            for sightseeing in form.cleaned_data.get('sightseeings'):
                Inclusion.objects.create(quote=self.quote, sightseeing=sightseeing, item_type='4_SIGHTSEEING')
            for visa in form.cleaned_data.get('visas'):
                Inclusion.objects.create(quote=self.quote, visa=visa, item_type='5_VISA')
        return HttpResponseRedirect(reverse('SalesApp:quote_detail', args=[self.quote_id]))

class QuoteItineraryView(InlineFormSetView):
    template_name = 'SalesApp/itinerary_form.html'
    model = Quote
    inline_model = Inclusion
    fields = ['title','day','itinerary_order']
    factory_kwargs = {'extra': 0, 'can_delete': False}

    def get_success_url(self):
        return reverse('SalesApp:quote_detail', kwargs={'pk': self.object.id})
    def get_formset_kwargs(self):
        kwargs = super(QuoteItineraryView, self).get_formset_kwargs()
        kwargs['queryset'] = self.object.inclusion_set.filter(itinerary_inclusion=True).order_by("day")
        return kwargs
    def formset_valid(self, formset):
        if self.object.inclusions_updated:
            self.object.itinerary_updated = True
        self.object.itinerary_exist = True
        self.object.save()
        return super(QuoteItineraryView, self).formset_valid(formset)

class QuotePricingView(UpdateView):
    template_name = 'SalesApp/quote/quote_price_form.html'
    model = Quote
    fields = ['manual_price','mark_up','discount','price']
    def get_context_data(self,**kwargs):
        context = super(QuotePricingView,self).get_context_data(**kwargs)
        pk = self.kwargs.get('pk')
        quote = Quote.objects.get(id=pk)
        inclusions_pricing_list, context['auto_price'] = quote.get_inclusions_price_list()
        return context
    def form_valid(self, form):
        self.object = form.save()
        self.object.price_valid = True
        if self.object.inclusions_updated and self.object.itinerary_updated:
            self.object.quote_valid = True
        self.object.save()
        return super().form_valid(form)


# ###############################
# #   PACKAGE VIEWS
# ###############################

class PackageCreateView(LoginRequiredMixin,CreateView):
    template_name = 'SalesApp/package/package_form.html'
    form_class = PackageForm
    model = Package

class PackageUpdateView(LoginRequiredMixin,UpdateView):
    template_name = 'SalesApp/package/package_form.html'
    form_class = PackageForm
    model = Package

class PackageListView(LoginRequiredMixin,FilterView):
        template_name = 'SalesApp/package/package_list.html'
        paginate_by = 10
        form_class = PackageForm
        filterset_class = PackageFilter
        ordering = ['id']

class PackageDetailView(LoginRequiredMixin,DetailView):
    template_name = 'SalesApp/package/package_detail.html'
    model = Package
    def get_context_data(self,**kwargs):
        context = super(PackageDetailView,self).get_context_data(**kwargs)
        pk = self.kwargs.get('pk')
        package = Package.objects.get(id=pk)
        hotel_groups = []
        for group in package.hotelgroup_set.all():
            hotel_groups.append(list(group.inclusion_set.all()))
        context['hotel_groups'] = hotel_groups
        context['inclusions'] = list(package.inclusion_set.filter(Q(optional=False) | Q(optional=True, include=True)))
        context['optionals_list'] = list(package.inclusion_set.filter(optional=True))
        context['itinerary'] = package.get_daywise_itinerary()
        context['pricing_list'] = list(package.pricing_set.all())
        return context

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
    form_class = HotelGroupForm
    formset_class = HotelGroupFS
    initial = [{'item_type': '1_HOTEL'},{'item_type': '1_HOTEL'},{'item_type': '1_HOTEL'}]
    factory_kwargs = {'extra': 3, 'can_delete': True}
    def get_success_url(self):
        return reverse('SalesApp:package_detail', kwargs={'pk': self.object.package.id})

class PackageInclusionBulkSelectView(FormView):
    template_name = 'SalesApp/inclusion_bulk_select.html'

    def setup(self, request, *args, **kwargs):
        self.request = request
        self.args = args
        self.kwargs = kwargs
        self.package_id = self.kwargs['pk']
        self.package = Package.objects.get(id=self.package_id)

    def get(self, request, *args, **kwargs):
        form = InclusionBulkSelectForm(object=self.package)
        return self.render_to_response(self.get_context_data(form=form))

    def post(self, request, *args, **kwargs):
        form = InclusionBulkSelectForm(self.request.POST, object=self.package)
        if form.is_valid():
            for transport in form.cleaned_data.get('transports'):
                Inclusion.objects.create(package=self.package, transport=transport, item_type='2_TRANSPORT')
            for transfer in form.cleaned_data.get('transfers'):
                Inclusion.objects.create(package=self.package, transfer=transfer, item_type='3_TRANSFER', itinerary_inclusion=True)
            for sightseeing in form.cleaned_data.get('sightseeings'):
                Inclusion.objects.create(package=self.package, sightseeing=sightseeing, item_type='4_SIGHTSEEING', itinerary_inclusion=True)
            for visa in form.cleaned_data.get('visas'):
                Inclusion.objects.create(package=self.package, visa=visa, item_type='5_VISA')
        return HttpResponseRedirect(reverse('SalesApp:package_detail', args=[self.package_id]))

class PackageInclusionView(InlineFormSetView):
    template_name = 'SalesApp/package/package_inclusion_form.html'
    model = Package
    inline_model = Inclusion
    form_class = PackageInclusionForm
    formset_class = PackageInclusionFS
    factory_kwargs = {'extra': 3, 'can_delete': True}

    def get_success_url(self):
        return reverse('SalesApp:package_detail', kwargs={'pk': self.object.id})
    def get_formset_kwargs(self):
        kwargs = super(PackageInclusionView, self).get_formset_kwargs()
        kwargs['queryset'] = self.object.inclusion_set.order_by("item_type")
        return kwargs

class PackageItineraryView(InlineFormSetView):
    template_name = 'SalesApp/itinerary_form.html'
    model = Package
    inline_model = Inclusion
    fields = ['title','day','itinerary_order']
    factory_kwargs = {'extra': 0, 'can_delete': False}

    def get_success_url(self):
        return reverse('SalesApp:package_detail', kwargs={'pk': self.object.id})
    def get_formset_kwargs(self):
        kwargs = super(PackageItineraryView, self).get_formset_kwargs()
        kwargs['queryset'] = self.object.inclusion_set.filter(itinerary_inclusion=True).order_by("day")
        return kwargs

class PackagePricingView(InlineFormSetView):
    template_name = 'SalesApp/pricing_form.html'
    model = Package
    inline_model = Pricing
    form_class = PricingForm
    factory_kwargs = {'extra': 1, 'can_delete': True}

    def get_success_url(self):
        return reverse('SalesApp:package_detail', kwargs={'pk': self.object.id})


###############################
#   LEAD VIEWS
###############################
class LeadListView(LoginRequiredMixin,LeadViewPM,FilterView):
    """ Generates a view to see details of all leads in a list. """
    template_name = 'SalesApp/lead/lead_list.html'
    paginate_by = 10
    form_class = LeadForm
    filterset_class = LeadFilter
    ordering = ['id']
    # def get_queryset(self):
    #     return Lead.objects.exclude(lead_status='BOOKED')

class LeadDetailView(LoginRequiredMixin,LeadViewPM,DetailView):
    template_name = 'SalesApp/lead/lead_detail.html'
    model = Lead
    def get_context_data(self,**kwargs):
        context = super(LeadDetailView,self).get_context_data(**kwargs)
        primary_key = self.kwargs.get('pk')
        context['booking'] = Booking.objects.get(quote__lead_id = primary_key)
        return context

class LeadCreateView(LoginRequiredMixin,LeadAddPM,CreateView):
    template_name = 'SalesApp/lead/lead_form.html'
    form_class = LeadForm
    model = Lead
    def get_initial(self):
        initial = super().get_initial()
        customer_id = self.request.GET.get("customer_id")
        initial['customer'] = Customer.objects.get(id=customer_id)
        return initial


class LeadUpdateView(LoginRequiredMixin,LeadEditPM,UpdateView):
    template_name = 'SalesApp/lead/lead_form.html'
    form_class = LeadForm
    model = Lead
