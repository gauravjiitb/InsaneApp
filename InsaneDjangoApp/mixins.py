from django.contrib.auth.mixins import UserPassesTestMixin,LoginRequiredMixin

from MarketingApp.models import Inquiry

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
