from django.contrib import admin
from django.urls import path,include
from django.views.generic import TemplateView

from SalesApp import views
from SalesApp.models import Customer,Lead

app_name = 'SalesApp'

urlpatterns = [
    # path('customer/list/',views.customer_list,name='customer_list'),
    path('customer/list/',views.CustomerListView.as_view(),name='customer_list'),
    path('customer/<int:pk>/',views.CustomerDetailView.as_view(),name='customer_detail'),
    path('customer/create/',views.CustomerCreateView.as_view(),name='customer_create'),
    path('customer/<int:pk>/update',views.CustomerUpdateView.as_view(),name='customer_update'),
    # path('customer/<int:pk>/delete/',views.CustomerDeleteView.as_view(),name='customer_delete'),
    path('lead/list/',views.LeadListView.as_view(),name='lead_list'),
    path('lead/<int:pk>/',views.LeadDetailView.as_view(),name='lead_detail'),
    path('lead/create/',views.LeadCreateView.as_view(),name='lead_create'),
    path('lead/<int:pk>/update',views.LeadUpdateView.as_view(),name='lead_update'),
]
