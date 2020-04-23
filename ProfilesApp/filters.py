import django_filters
from django.contrib.auth import get_user_model
from ProfilesApp.models import Customer


class CustomerFilter(django_filters.FilterSet):
    # def get_names():
    #     names = ()
    #     User = get_user_model()
    #     users = User.objects.filter(is_staff=False)
    #     for user in users:
    #         names += (user.name),
    #     return names
    # name = django_filters.ChoiceFilter(choices=get_names)
    User = get_user_model()
    user = django_filters.ModelChoiceFilter(queryset=User.objects.all())

    class Meta:
        model = Customer
        fields = {
            'user':[],
        }
