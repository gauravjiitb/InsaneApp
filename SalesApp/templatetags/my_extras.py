from django import template
from django.contrib.auth.models import Group

register = template.Library()

@register.filter(name='has_group')
def has_group(user, group_name):
    group = Group.objects.get(name=group_name)
    return True if group in user.groups.all() else False

@register.filter(name='add_class')
def add_class(value, arg):
    return value.as_widget(attrs={'class': arg})

@register.filter(name='get_model_name')
def get_model_name(value):
  return value.__class__.__name__

@register.filter(name='csv_str_to_list')
def csv_str_to_list(value):
  return value.split(',')
