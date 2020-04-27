from django.shortcuts import render,redirect
from django.views.generic import ListView,DetailView,CreateView,UpdateView


from ContentApp.models import Transfer
from ContentApp.forms import TransferForm

# Create your views here.

class TransferCreateView(CreateView):
    form_class = TransferForm
    model = Transfer
