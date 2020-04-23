from django.contrib import admin
from django.urls import path,include

from MarketingApp import views

app_name = 'MarketingApp'


urlpatterns = [
    path('inquiry/create/',views.InquiryCreateView.as_view(),name='inquiry_create'),
    path('inquiry/<int:pk>/update/',views.InquiryUpdateView.as_view(),name='inquiry_update'),
    path('inquiries/',views.InquiryListView.as_view(),name='inquiry_list'),
    path('inquiry/<int:pk>/',views.InquiryDetailView.as_view(),name='inquiry_detail'),
    path('inquiry/<int:pk>/assignment',views.InquiryAssignView.as_view(),name='inquiry_assign'),
]
