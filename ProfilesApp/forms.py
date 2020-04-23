from django import forms
from django.contrib.auth import get_user_model
from django.db import transaction

from phonenumber_field.formfields import PhoneNumberField

from ProfilesApp.models import Customer

###############################################################

class CustomerCreateForm(forms.Form):
    name = forms.CharField(max_length=100,required=True)
    email = forms.EmailField(required=True)
    phone = PhoneNumberField(required=True)

    def clean(self):
        User = get_user_model()
        cleaned_data = super().clean()
        email = cleaned_data.get("email")
        username = email
        # username = email if email else phone (Will be useful if we give option of using phone also unique username in future)
        # if not email and not phone:
        #     raise forms.ValidationError("Either Email or Phone Number is required")
        if User.objects.filter(username=username).exists():
            raise forms.ValidationError("Your details are already registered with us.")

    @transaction.atomic
    def save(self):
        User = get_user_model()
        cleaned_data = super().clean()
        email = cleaned_data.get("email")
        phone = cleaned_data.get("phone")
        name = cleaned_data.get("name")
        username = email
        # username = email if email else phone
        password = 'hdgtrkdb@75749'
        user = User.objects.create_user(username=username,name=name,email=email,phone=phone,password=password)
        customer = Customer.objects.create(user=user)
        # add more attributes to customer if needed in future
        return user


class CustomerUpdateForm(forms.Form):
    name = forms.CharField(max_length=100,required=True)
    email = forms.EmailField(required=True)
    phone = PhoneNumberField(required=True)

    @transaction.atomic
    def save(self,pk):
        customer = Customer.objects.get(id=pk)
        user = customer.user
        cleaned_data = super().clean()
        user.email = cleaned_data.get("email")
        user.phone = cleaned_data.get("phone")
        user.name = cleaned_data.get("name")
        user.username = user.email
        user.save()
        return user




#####################################################################
# Below is the code for creating User from AbstractBaseUser
#####################################################################
#
# class AddUserForm(forms.ModelForm):
#     """
#     New User Form. Requires password confirmation.
#     """
#     password1 = forms.CharField(label='Password', widget=forms.PasswordInput)
#     password2 = forms.CharField(label='Confirm password', widget=forms.PasswordInput)
#     class Meta:
#         model = User
#         fields = ('email', 'name')
#
#     def clean_password2(self):
#         # Check that the two password entries match
#         password1 = self.cleaned_data.get("password1")
#         password2 = self.cleaned_data.get("password2")
#         if password1 and password2 and password1 != password2:
#             raise forms.ValidationError("Passwords do not match")
#         return password2
#
#     def save(self, commit=True):
#         # Save the provided password in hashed format
#         user = super().save(commit=False)
#         user.set_password(self.cleaned_data["password1"])
#         if commit:
#             user.save()
#         return user
#
#
# class UpdateUserForm(forms.ModelForm):
#     """
#     Update User Form. Doesn't allow changing password in the Admin.
#     """
#     password = ReadOnlyPasswordHashField()
#     class Meta:
#         model = User
#         fields = ('email', 'password', 'name', 'is_active','is_staff')
#
#     def clean_password(self):
#         # Password can't be changed in the admin.
#         # Regardless of what the user provides, return the initial value.
#         # This is done here, rather than on the field, because the field does not have access to the initial value.
#         return self.initial["password"]
