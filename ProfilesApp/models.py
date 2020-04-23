from django.conf import settings
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.conf import settings

from phonenumber_field.modelfields import PhoneNumberField
########################################################################

# Create your models here.

class User(AbstractUser):
    name = models.CharField(max_length=100)
    phone = PhoneNumberField(unique=True)
    email = models.EmailField(unique=True)

    def __str__(self):
        return self.name

        

class Customer(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.PROTECT)

    def get_absolute_url(self):
        return reverse("ProfilesApp:customer_detail",kwargs={'pk':self.pk})

    def __str__(self):
        return self.user.name



class Staff(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL,on_delete=models.PROTECT)
    manager = models.ForeignKey('self',related_name='Reportees',on_delete=models.PROTECT,blank=True,null=True)

    def __str__(self):
        return self.user.name



#####################################################################
# Below is the code for creating User from AbstractBaseUser
#####################################################################
#
# class User(AbstractBaseUser, PermissionsMixin):
#     email = models.EmailField(verbose_name=_('email address'), max_length=255, unique=True)
#
#     # password field supplied by AbstractBaseUser
#     # last_login field supplied by AbstractBaseUser
#     name = models.CharField(_('name'), max_length=100)
#
#
#     is_active = models.BooleanField(
#         _('active'),
#         default=True,
#         help_text=_(
#             'Designates whether this user should be treated as active. '
#             'Unselect this instead of deleting accounts.'
#         ),
#     )
#     is_staff = models.BooleanField(
#         _('staff status'),
#         default=False,
#         help_text=_(
#             'Designates whether the user can log into this admin site.'
#         ),
#     )
#     # is_superuser field provided by PermissionsMixin
#     # groups field provided by PermissionsMixin
#     # user_permissions field provided by PermissionsMixin
#
#     date_joined = models.DateTimeField(
#         _('date joined'), default=timezone.now
#     )
#
#     objects = UserManager()
#
#     USERNAME_FIELD = 'email'
#     REQUIRED_FIELDS = ['name']
#
#     def get_full_name(self):
#         """
#         Return the Name of User.
#         """
#         # full_name = '%s %s' % (self.first_name, self.last_name)
#         return self.name.strip()
#
#     def __str__(self):
#         return '{} <{}>'.format(self.get_full_name(), self.email)
#
#     def has_perm(self, perm, obj=None):
#         "Does the user have a specific permission?"
#         # Simplest possible answer: Yes, always
#         return True
#
#     def has_module_perms(self, app_label):
#         "Does the user have permissions to view the app `app_label`?"
#         # Simplest possible answer: Yes, always
#         return True
#
