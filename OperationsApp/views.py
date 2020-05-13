from itertools import chain
import json

from django.shortcuts import render
from django.contrib.auth.mixins import LoginRequiredMixin,UserPassesTestMixin
from django.views.generic import TemplateView,ListView,DetailView,CreateView,UpdateView
from django.urls import reverse_lazy,reverse

from django.core.mail import send_mail

from django_filters.views import FilterView
from extra_views import InlineFormSetView


from OperationsApp.models import Booking, BookingItem, Traveler
from SalesApp.models import Lead, Quote
from OperationsApp.forms import BookingForm, BookingItemForm, TravelerForm
from OperationsApp.filters import BookingFilter
from AccountsApp.models import PendingPayment,TripPayment

###############################
#   CUSTOMER VIEWS
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
        context['inclusions_pricing_list'], context['auto_price'] = booking.quote.get_quote_price_list()
        context['booking_items'] = list(booking.bookingitem_set.all())
        context['itinerary'] = json.loads(booking.itinerary)
        return context


class BookingCreateView(LoginRequiredMixin,CreateView):
    form_class = BookingForm
    model = Booking

    def get_initial(self):
        """
        Returns the initial data to use for forms on this view.
        """
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
        objects_list = self.object.quote.get_included_objects()
        for object in objects_list:
            if object.__class__.__name__ == 'Transport':
                BookingItem.objects.create(booking=self.object,item_type='TRANSPORT',detail=object.__str__(),display_order=3)
            elif object.__class__.__name__ == 'Transfer':
                BookingItem.objects.create(booking=self.object,item_type='TRANSFER',detail=object.__str__(),display_order=5)
            elif object.__class__.__name__ == 'Sightseeing':
                BookingItem.objects.create(booking=self.object,item_type='SIGHTSEEING',detail=object.__str__(),display_order=6)
            elif object.__class__.__name__ == 'Visa':
                BookingItem.objects.create(booking=self.object,item_type='VISA',detail=object.__str__(),display_order=7)
            elif object.__class__.__name__ == 'Insurance':
                BookingItem.objects.create(booking=self.object,item_type='INSURANCE',detail=object.__str__(),display_order=8)
            elif object.__class__.__name__ == 'Inclusion':
                if object.item_type == 'FLIGHT':
                    BookingItem.objects.create(booking=self.object,item_type='FLIGHT',detail=object.details,display_order=1)
                elif object.item_type == 'HOTEL':
                    detail = '{} - {} | {} | {} | {}({})'.format(object.checkin_date.strftime("%d %b"), object.checkout_date.strftime("%d %b"),
                                                                    object.hotel.city, object.hotel.name, object.room_type, object.no_of_rooms)
                    BookingItem.objects.create(booking=self.object,item_type='HOTEL',detail=detail,display_order=2)
                elif object.item_type == 'OTHER':
                    BookingItem.objects.create(booking=self.object,item_type='OTHER',detail=object.name,display_order=9)
                elif object.item_type == 'EXCLUSION':
                    BookingItem.objects.create(booking=self.object,item_type='EXCLUSION',detail=object.details,display_order=10)

        itinerary_objects_list = self.object.quote.get_daywise_itinerary_objects()
        itinerary = []
        for day in itinerary_objects_list:
            day_plan = []
            for object in day:
                if object.__class__.__name__ == 'Inclusion':
                    day_plan.append(object.details)
                else:
                    day_plan.append(object.description)
            itinerary.append('\n\n'.join(day_plan))
        self.object.itinerary = json.dumps(itinerary)
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
