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

    path('ajax/quote/load-cities/', views.quote_load_cities, name='ajax_quote_load_cities'),
    path('ajax/quote/load-hotels/', views.quote_load_hotels, name='ajax_quote_load_hotels'),
    path('ajax/quote/load-transfers/', views.quote_load_transfers, name='ajax_quote_load_transfers'),
    path('ajax/quote/load-sightseeings/', views.quote_load_sightseeings, name='ajax_quote_load_sightseeings'),
    path('ajax/package/load-hotelgroups/',views.package_load_hotelgroups,name='ajax_package_load_hotelgroups'),

    path('quote/create/',views.QuoteCreateView.as_view(),name='quote_create'),
    path('quote/<int:pk>/update',views.QuoteUpdateView.as_view(),name='quote_update'),
    path('quote/<int:pk>/',views.QuoteDetailView.as_view(),name='quote_detail'),
    path('quotes/',views.QuoteListView.as_view(),name='quote_list'),
    path('quote/<int:pk>/inclusions',views.QuoteInclusionView.as_view(),name='quote_inclusions'),
    path('quote/<int:pk>/itinerary',views.QuoteItineraryView.as_view(),name='quote_itinerary'),
    path('quote/<int:pk>/select-packages',views.quote_package_selection,name='quote_package_selection'),
    path('quote/<int:pk>/select-inclusions',views.QuoteInclusionBulkSelectView.as_view(), name='quote_inclusions_bulk_select'),
    path('quote/<int:pk>/pricing',views.QuotePricingView.as_view(),name='quote_pricing'),

    # path('quote/inclusions/create/',views.FlexInclusionsCreateView.as_view(),name='flex_inclusions_create'),
    # path('quote/inclusions/update/',views.FlexInclusionsUpdateView.as_view(),name='flex_inclusions_update'),
    # path('quote/itinerary/create/',views.FlexItineraryCreateView.as_view(),name='flex_itinerary_create'),
    # path('quote/itinerary/update/',views.FlexItineraryUpdateView.as_view(),name='flex_itinerary_update'),

    path('package/create/',views.PackageCreateView.as_view(),name='package_create'),
    path('packages/',views.PackageListView.as_view(),name='package_list'),
    path('package/<int:pk>/',views.PackageDetailView.as_view(),name='package_detail'),
    path('package/<int:pk>/update',views.PackageUpdateView.as_view(),name='package_update'),
    path('package/<int:pk>/hotel-option/create',views.HotelGroupCreateView.as_view(),name='hotel_option_create'),
    path('package/hotel-options/<int:pk>/',views.PackageHotelsCreateView.as_view(),name='package_hotels_create'),
    path('package/<int:pk>/select-inclusions',views.PackageInclusionBulkSelectView.as_view(), name='package_inclusions_bulk_select'),
    path('package/<int:pk>/inclusions/',views.PackageInclusionView.as_view(),name='package_inclusions'),
    path('package/<int:pk>/itinerary/',views.PackageItineraryView.as_view(),name='package_itinerary'),
    path('package/<int:pk>/pricing/',views.PackagePricingView.as_view(),name='package_pricing'),
    # path('package-optionals/<int:pk>/pricing',views.PackageOptionalsPricingView.as_view(),name='package_optionals_pricing'),
]
