from django.contrib import admin
from django.urls import path,include

from ContentApp import views

app_name = 'ContentApp'


urlpatterns = [
    path('transfer/create/',views.TransferCreateView.as_view(),name='transfer_create'),
]
