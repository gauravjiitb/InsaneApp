from django.contrib import admin
from django.urls import path,include

from OperationsApp import views

app_name = 'OperationsApp'

urlpatterns = [
    path('booking/list/',views.BookingListView.as_view(),name='booking_list'),
    path('booking/<int:pk>/',views.BookingDetailView.as_view(),name='booking_detail'),
    path('booking/create/',views.BookingCreateView.as_view(),name='booking_create'),
    path('booking/<int:pk>/update/',views.BookingUpdateView.as_view(),name='booking_update'),

    path('booking/<int:pk>/booking-items/update/',views.BookingItemUpdateView.as_view(),name='booking_item_update'),
]
