from django.contrib import admin
from django.urls import path,include
from django.views.generic import TemplateView

from SalesApp import views
from SalesApp.models import Customer,Lead

app_name = 'SalesApp'

urlpatterns = [
    path('lead/list/',views.LeadListView.as_view(),name='lead_list'),
    path('lead/<int:pk>/',views.LeadDetailView.as_view(),name='lead_detail'),
    path('lead/create/',views.LeadCreateView.as_view(),name='lead_create'),
    path('lead/<int:pk>/update',views.LeadUpdateView.as_view(),name='lead_update'),

    # path('quote/create/',views.quote_create_update,name='quote_create'),
    path('ajax/quote/load-cities/', views.quote_load_cities, name='ajax_quote_load_cities'),
    path('ajax/quote/load-hotels/', views.quote_load_hotels, name='ajax_quote_load_hotels'),
    path('ajax/quote/load-transfers/', views.quote_load_transfers, name='ajax_quote_load_transfers'),
    path('ajax/quote/load-sightseeings/', views.quote_load_sightseeings, name='ajax_quote_load_sightseeings'),
    # path('quote/create/pax-details/',views.quote_pax_details,name='quote_create_pax_details'),

    # path('quote/<int:pk>/update',views.quote_create_update,name='quote_update'),
    path('quote/create/',views.QuoteCreateView.as_view(),name='quote_create'),
    path('quote/<int:pk>/update',views.QuoteUpdateView.as_view(),name='quote_update'),
    path('quote/<int:pk>/',views.QuoteDetailView.as_view(),name='quote_detail'),

    path('quote/inclusions/create/',views.FlexInclusionsCreateView.as_view(),name='flex_inclusions_create'),
    path('quote/inclusions/update/',views.FlexInclusionsUpdateView.as_view(),name='flex_inclusions_update'),
    path('quote/itinerary/create/',views.FlexItineraryCreateView.as_view(),name='flex_itinerary_create'),
    path('quote/itinerary/update/',views.FlexItineraryUpdateView.as_view(),name='flex_itinerary_update'),

    path('quote/inclusions/',views.CustomInclusionsView.as_view(),name='custom_inclusions'),
    path('quote/itinerary/',views.CustomItineraryView.as_view(),name='custom_itinerary'),
]
