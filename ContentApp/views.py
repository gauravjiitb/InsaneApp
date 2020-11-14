from django.shortcuts import render,redirect,reverse,HttpResponseRedirect
from django.views.generic import ListView,DetailView,CreateView,UpdateView,FormView
from django.contrib.auth.mixins import LoginRequiredMixin,UserPassesTestMixin

from ContentApp.models import Transfer, Theme, Tag
from ContentApp.forms import TransferForm

# Create your views here.

class TransferCreateView(LoginRequiredMixin,CreateView):
    template_name = 'ContentApp/generic_form.html'
    form_class = TransferForm
    model = Transfer

class ThemeCreateView(LoginRequiredMixin,CreateView):
    template_name = 'ContentApp/generic_form_file_upload.html'
    model = Theme
    fields = ['name', 'image']
    success_url = ''

class ThemeUpdateView(LoginRequiredMixin,UpdateView):
    template_name = 'ContentApp/generic_form_file_upload.html'
    model = Theme
    fields = ['name', 'image']
    success_url = ''

class TagCreateView(LoginRequiredMixin,CreateView):
    template_name = 'ContentApp/generic_form_file_upload.html'
    model = Tag
    fields = ['name', 'image']
    # success_url = ''

class TagUpdateView(LoginRequiredMixin,UpdateView):
    template_name = 'ContentApp/generic_form_file_upload.html'
    model = Tag
    fields = ['name', 'image']
    # success_url = reverse('dashboard')
