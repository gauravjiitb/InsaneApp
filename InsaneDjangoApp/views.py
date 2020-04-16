from django.shortcuts import render,redirect
from django.contrib.auth.mixins import LoginRequiredMixin,UserPassesTestMixin
from django.views.generic import TemplateView
from django.urls import reverse_lazy,reverse


def DashboardView(request):
    template_name = 'dashboard.html'
    return render(request,template_name)
