from django.contrib import admin
# from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

from ProfilesApp.models import User,Customer,Staff
# from ProfilesApp.forms import AddUserForm,UpdateUserForm


##############################################################

class UserAdmin(admin.ModelAdmin):
    list_display = ('id','name','username')

#
class CustomerAdmin(admin.ModelAdmin):
    list_display = ('id','user')
# #     list_select_related = ('Lead',)
#
class StaffAdmin(admin.ModelAdmin):
    list_display = ('id','user')

# Register your models here.

admin.site.register(User,UserAdmin)
admin.site.register(Customer,CustomerAdmin)
admin.site.register(Staff,StaffAdmin)



#####################################################################
# Below is the code for creating User from AbstractBaseUser
#####################################################################

# class UserAdmin(BaseUserAdmin):
#     # The forms to add and change user instances.
#     form = UpdateUserForm
#     add_form = AddUserForm
#
#     # The fields to be used in displaying the User model.
#     # These override the definitions on the base UserAdmin
#     # that reference specific fields on auth.User.
#     list_display = ('name', 'email', 'is_staff')
#     list_filter = ('is_staff', )
#     fieldsets = (
#         (None, {'fields': ('email', 'password')}),
#         ('Personal info', {'fields': ('name',)}),
#         ('Permissions', {'fields': ('is_active', 'is_staff','groups')}),
#     )
#     # add_fieldsets is not a standard ModelAdmin attribute. UserAdmin
#     # overrides get_fieldsets to use this attribute when creating a user.
#     add_fieldsets = (
#         (None, {
#                 'classes': ('wide',),
#                 'fields': ('email', 'name', 'password1', 'password2')
#             }),
#     )
#     search_fields = ('email', 'name')
#     ordering = ('name', 'email')
#     filter_horizontal = ()
