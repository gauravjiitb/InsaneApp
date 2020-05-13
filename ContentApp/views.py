from django.shortcuts import render,redirect,reverse,HttpResponseRedirect
from django.views.generic import ListView,DetailView,CreateView,UpdateView,FormView
from django.contrib.auth.mixins import LoginRequiredMixin,UserPassesTestMixin

from ContentApp.models import Transfer
from ContentApp.forms import TransferForm

# Create your views here.

class TransferCreateView(LoginRequiredMixin,CreateView):
    form_class = TransferForm
    model = Transfer
