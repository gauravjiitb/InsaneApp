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
]
