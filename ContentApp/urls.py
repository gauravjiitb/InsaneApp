from django.contrib import admin
from django.urls import path,include

from ContentApp import views

app_name = 'ContentApp'


urlpatterns = [
    path('transfer/create/',views.TransferCreateView.as_view(),name='transfer_create'),

    path('theme/create/',views.ThemeCreateView.as_view(),name='theme_create'),
    path('theme/<int:pk>/update/',views.ThemeUpdateView.as_view(),name='theme_update'),
    path('tag/create/',views.TagCreateView.as_view(),name='tag_create'),
    path('tag/<int:pk>/update/',views.TagUpdateView.as_view(),name='tag_update'),
]
