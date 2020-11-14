from itertools import chain
import json
from datetime import timedelta

from django.shortcuts import render, HttpResponseRedirect
from django.contrib.auth.mixins import LoginRequiredMixin,UserPassesTestMixin
from django.views.generic import TemplateView,ListView,DetailView,CreateView,UpdateView, FormView
from django.urls import reverse_lazy,reverse
from django.core.mail import send_mail

from django_filters.views import FilterView
from extra_views import InlineFormSetView, ModelFormSetView

from ProfilesApp.models import Traveler
from OperationsApp.models import Booking, BookingItem
from SalesApp.models import Lead, Quote
from AccountsApp.models import PendingPayment,TripPayment
from OperationsApp.forms import BookingForm, BookingItemForm, AddTravelersFS
from OperationsApp.filters import BookingFilter

###############################
#   BOOKING VIEWS
###############################

class BookingListView(LoginRequiredMixin,FilterView):
    template_name = 'OperationsApp/booking_list.html'
    paginate_by = 5
    form_class = BookingForm
    filterset_class = BookingFilter

class BookingDetailView(LoginRequiredMixin,DetailView):
    model = Booking
    context_object_name = 'booking'

    def get_context_data(self,**kwargs):
        context = super(BookingDetailView,self).get_context_data(**kwargs)
        primary_key = self.kwargs.get('pk')
        pending_payments = PendingPayment.objects.filter(booking = primary_key,vendor__isnull=True)
        trip_payments = TripPayment.objects.filter(booking = primary_key,vendor__isnull=True)
        context['payments'] = sorted(chain(pending_payments, trip_payments),key=lambda data: data.date)
        booking = Booking.objects.get(id=primary_key)
        context['booking_items'] = list(booking.bookingitem_set.all())
        context['itinerary'] = json.loads(booking.itinerary)
        return context

class BookingCreateView(LoginRequiredMixin,CreateView):
    form_class = BookingForm
    model = Booking

    def get_initial(self):
        initial = super().get_initial()
        try:
            quote_id = self.request.GET.get("quote_id")
            initial['quote'] = Quote.objects.get(id=quote_id)
        except:
            pass
        return initial

    def form_valid(self, form):
        """If the form is valid, save the associated model."""
        self.object = form.save()
        for inclusion in self.object.quote.inclusion_set.exclude(include=False):
            date = self.object.quote.start_date + timedelta(days=inclusion.day-1) if inclusion.day else None
            BookingItem.objects.create(booking=self.object, item_type=inclusion.item_type, display_handle=inclusion.__str__(),
                                        date=date, inclusion=inclusion)
        itinerary_objects_list = self.object.quote.get_daywise_itinerary()
        self.object.itinerary = json.dumps(itinerary_objects_list)
        self.object.save()
        return super().form_valid(form)

class BookingUpdateView(LoginRequiredMixin,UpdateView):
    form_class = BookingForm
    model = Booking

class BookingItemUpdateView(LoginRequiredMixin,InlineFormSetView):
    template_name = 'OperationsApp/bookingitem_form.html'
    model = Booking
    inline_model = BookingItem
    form_class = BookingItemForm
    factory_kwargs = {'extra': 0, 'can_delete': False}
    def get_success_url(self):
        return reverse('OperationsApp:booking_detail', kwargs={'pk': self.object.id})
    def get_formset_kwargs(self):
        kwargs = super(BookingItemUpdateView, self).get_formset_kwargs()
        kwargs['queryset'] = self.object.bookingitem_set.order_by("item_type")
        return kwargs

class AddTravelersView(LoginRequiredMixin,FormView):
    template_name = 'OperationsApp/add_travelers.html'

    def setup(self, request, *args, **kwargs):
        self.request = request
        self.args = args
        self.kwargs = kwargs
        self.booking_id = self.kwargs['pk']
        self.booking = Booking.objects.get(id=self.booking_id)
        self.customer = self.booking.quote.lead.customer

    def get(self, request, *args, **kwargs):
        form =[]
        formset = AddTravelersFS(queryset=self.booking.travelers.all())
        return self.render_to_response(self.get_context_data(form=form, formset=formset))

    def post(self, request, *args, **kwargs):
        form =[]
        formset = AddTravelersFS(self.request.POST)
        if formset.is_valid():
            instances = formset.save()
            for instance in instances:
                self.booking.travelers.add(instance)
                self.booking.save()
                self.customer.travelers.add(instance)
                self.customer.save()
            return HttpResponseRedirect(reverse('OperationsApp:booking_detail', args=[self.booking_id]))
        else:
            return self.render_to_response(self.get_context_data(form=form, formset=formset))
