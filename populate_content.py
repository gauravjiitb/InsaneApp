import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE','InsaneDjangoApp.settings')
import django
django.setup()
import csv
import random

from ContentApp.models import Destination,City,Hotel

def populate_destinations():
    f = open("destinations_data.csv", "r")
    reader = csv.reader(f)
    lines = []
    for row in reader:
        lines.append(row)
    lines.pop(0)
    for line in lines:
        pass
        # Destination.objects.create(name=data[0],description=data[1],region=[2])


def populate_content():
    populate_destinations()

if __name__ == '__main__':
    print("Populating Script!")
    populate_content()
    print("Populating Complete!")
