from django.contrib import admin
from django.urls import path,include

from ProfilesApp import views
from ProfilesApp.models import Customer

app_name = 'ProfilesApp'


urlpatterns = [
    path('customer/list/',views.CustomerListView.as_view(),name='customer_list'),
    path('customer/<int:pk>/',views.CustomerDetailView.as_view(),name='customer_detail'),
    path('customer/create/',views.CustomerCreateView.as_view(),name='customer_create'),
    path('customer/<int:pk>/update',views.CustomerUpdateView.as_view(),name='customer_update'),
    path('traveler/create/',views.TravelerCreateView.as_view(),name='traveler_create'),
    path('traveler/<int:pk>/update',views.TravelerUpdateView.as_view(),name='traveler_update'),
]
