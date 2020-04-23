from django.shortcuts import render,redirect
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView
from django.urls import reverse_lazy,reverse

from InsaneDjangoApp.mixins import StaffRequiredMixin


class DashboardView(StaffRequiredMixin,TemplateView):
    template_name = 'dashboard.html'
