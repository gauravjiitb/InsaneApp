from django.contrib.auth.mixins import UserPassesTestMixin,LoginRequiredMixin

from ProfilesApp.models import Staff
from MarketingApp.models import Inquiry
from SalesApp.models import Lead


def get_reportees(staff, reportees):
    reportees.append(staff)
    for st in Staff.objects.filter(manager=staff):
        get_reportees(st, reportees)
    return reportees

def staff_ownership_check(staff, object):
    if object.owner == staff:
        return True
    else:
        return (object.owner in get_reportees(staff, []))



class LeadAddPM(UserPassesTestMixin):
    def test_func(self):
        if self.request.user.has_perm('SalesApp.add_lead'):
            return True

class LeadEditPM(UserPassesTestMixin):
    def test_func(self):
        pk = self.kwargs.get('pk')
        lead = Lead.objects.get(id=pk)
        if self.request.user.has_perm('SalesApp.edit_lead') and staff_ownership_check(self.request.user.staff, lead) and lead.lead_status != 'BOOKED':
            return True

class LeadViewPM(UserPassesTestMixin):
    def test_func(self):
        if self.request.user.has_perm('SalesApp.view_lead'):
            return True





class InquiryUpdatePermissionMixin(UserPassesTestMixin):
    def test_func(self):
        pk = self.kwargs.get('pk')
        # self.request.user.has_perm('MarketingApp.change_inquiry')   // alternate method to check permission if assigned explicitly
        if self.request.user.groups.filter(name='Marketing').exists():
            if self.request.user.staff in Inquiry.objects.get(id=pk).assigned_staff.all():
                return True

class InquiryDetailPermissionMixin(UserPassesTestMixin):
    def test_func(self):
        pk = self.kwargs.get('pk')
        if self.request.user.staff in Inquiry.objects.get(id=pk).assigned_staff.all():
            return True

class AssignPermissionMixin(UserPassesTestMixin):
    def test_func(self):
        return self.request.user.groups.filter(name='AdminUsers').exists()

class StaffRequiredMixin(UserPassesTestMixin):
    def test_func(self):
        return self.request.user.is_staff

class MarketingStaffMixin(UserPassesTestMixin):
    def test_func(self):
        return self.request.user.groups.filter(name='Marketing').exists()

class SalesSatffMixin(UserPassesTestMixin):
    def test_func(self):
        return self.request.user.groups.filter(name='Sales').exists()

class OperationsStaffMixin(UserPassesTestMixin):
    def test_func(self):
        return self.request.user.groups.filter(name='Operations').exists()

class AccountsStaffMixin(UserPassesTestMixin):
    def test_func(self):
        return self.request.user.groups.filter(name='Accounts').exists()
