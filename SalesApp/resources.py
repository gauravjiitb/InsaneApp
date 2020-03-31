import django
from django.conf import settings

if not settings.configured:
    settings.configure(DEBUG=True)
django.setup()

from import_export import resources
from .models import Customer,Lead

class CustomerResource(resources.ModelResource):
    class Meta:
        model = Customer
