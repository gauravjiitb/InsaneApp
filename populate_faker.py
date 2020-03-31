import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE','InsaneDjangoApp.settings')

import django
django.setup()

import random
from SalesApp.models import Customer,Lead
from OperationsApp.models import Booking
from faker import Faker

fakegen = Faker()

def populate(N=20):

    for entry in range(N):
        fake_name = fakegen.name()
        fake_em = fakegen.email()
        fake_ph = random.randint(123456789,999999999)

        lead_source_choices = ['FNF','TT','CRF','RPC','FBAD','B2B','WEB']
        lead_status_choices = ['NEW','QUOTED','BOOKED']
        fake_dest = fakegen.country()
        fake_src = random.choice(lead_source_choices)
        fake_st = random.choice(lead_status_choices)
        fake_srcid = random.randint(1111,9999)
        fake_remarks = fakegen.street_name()
        fake_crdate = fakegen.date()

        status_choices = ['BOOKED','TRAVELLED','CLOSED']
        fake_status = random.choice(status_choices)
        fake_bkdate = fakegen.date()
        fake_trdate = fakegen.date()
        fake_bdest = fakegen.country()
        fake_saleamt = random.randint(11111,99999)
        fake_projrev = random.randint(1111,9999)
        fake_actrev = random.randint(1111,9999)
        fake_tcs = random.randint(111,999)
        fake_gst = random.randint(111,999)
        fake_com = random.randint(111,999)

        fakecustomer = Customer.objects.get_or_create(name=fake_name, email=fake_em, phone=fake_ph)[0]
        fakelead = Lead.objects.get_or_create(customer=fakecustomer,destinations=fake_dest,lead_source=fake_src,lead_source_id=fake_srcid,
                    lead_status=fake_st,remarks=fake_remarks,creation_date=fake_crdate)[0]
        fakebooking = Booking.objects.get_or_create(lead=fakelead,status=fake_status,booking_date=fake_bkdate,travel_date=fake_trdate,
                        booked_destinations=fake_bdest,sale_amount=fake_saleamt,projected_revenue=fake_projrev,
                        actual_revenue=fake_actrev,tcs_amount=fake_tcs,gst_amount=fake_gst,commission_paid=fake_com)[0]

if __name__ == '__main__':
    print("Populating Script!")
    populate(20)
    print("Populating Complete!")
