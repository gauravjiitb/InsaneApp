from django.shortcuts import render,redirect
from django.contrib.auth.mixins import LoginRequiredMixin,UserPassesTestMixin
from django.views.generic import ListView,DetailView,CreateView,UpdateView
from django.contrib.auth.models import Permission

from django_filters.views import FilterView

from InsaneDjangoApp.mixins import StaffRequiredMixin,MarketingStaffMixin,InquiryDetailPermissionMixin,InquiryUpdatePermissionMixin,AssignPermissionMixin
from MarketingApp.models import Inquiry
from ProfilesApp.models import Staff
from MarketingApp.forms import InquiryForm,InquiryAssignForm
from MarketingApp.filters import InquiryFilter

# Create your views here.

class InquiryCreateView(LoginRequiredMixin, StaffRequiredMixin, CreateView):
    model = Inquiry
    form_class = InquiryForm

    def form_valid(self, form):
        inquiry = form.save(commit=False)
        staff = self.request.user.staff

        if self.request.user.groups.filter(name='Marketing').exists():
            inquiry.owner = staff
        else:
            inquiry.owner = Staff.objects.filter(user__groups__name='AdminUsers')[1]

        inquiry.save()
        while staff:
            inquiry.assigned_staff.add(staff)
            staff = staff.manager
        return redirect(inquiry)


class InquiryUpdateView(LoginRequiredMixin, InquiryUpdatePermissionMixin, UpdateView):
    model = Inquiry
    form_class = InquiryForm


class InquiryDetailView(LoginRequiredMixin, InquiryDetailPermissionMixin, DetailView):
    model = Inquiry
    

class InquiryListView(LoginRequiredMixin, StaffRequiredMixin, FilterView):
    model = Inquiry
    template_name = 'MarketingApp/inquiry_list.html'
    paginate_by = 10
    form_class = InquiryForm
    filterset_class = InquiryFilter
    ordering = ['creation_date']

    def get_queryset(self):
        staff = self.request.user.staff
        return Inquiry.objects.filter(assigned_staff=staff)


class InquiryAssignView(LoginRequiredMixin,AssignPermissionMixin,UpdateView):
    model = Inquiry
    form_class = InquiryAssignForm

    def form_valid(self, form):
        inquiry = form.save(commit=False)
        staff = inquiry.owner if inquiry.owner else False
        inquiry.save()
        while staff:
            inquiry.assigned_staff.add(staff)
            staff = staff.manager
        return redirect(inquiry)
