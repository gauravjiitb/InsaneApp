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

    path('quote/create/',views.quote_create,name='quote_create'),
    path('ajax/quote/load-cities/', views.quote_load_cities, name='ajax_quote_load_cities'),
    path('ajax/quote/load-hotels/', views.quote_load_hotels, name='ajax_quote_load_hotels'),
    path('ajax/quote/load-transfers/', views.quote_load_transfers, name='ajax_quote_load_transfers'),
    path('ajax/quote/load-sightseeings/', views.quote_load_sightseeings, name='ajax_quote_load_sightseeings'),
    # path('ajax/quote/load-cities/', views.quote_load_cities, name='ajax_quote_load_transfers'),
    # path('ajax/quote/load-cities/', views.quote_load_cities, name='ajax_quote_load_sightseeings'),
    path('quote/create/pax-details/',views.quote_pax_details,name='quote_create_pax_details'),

    path('quote/<int:pk>/update',views.quote_create,name='quote_update'),
]
