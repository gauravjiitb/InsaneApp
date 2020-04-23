import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE','InsaneDjangoApp.settings')

import django
django.setup()

import random
from django.contrib.auth import get_user_model
from django.db import transaction
from django.contrib.auth.models import Group, Permission

from ContentApp.models import Destination, Vendor
from MarketingApp.models import LeadSource,Inquiry
from ProfilesApp.models import Customer,Staff
from SalesApp.models import Lead
from OperationsApp.models import Booking
from AccountsApp.models import Account,Transaction,TransactionHead,TripPayment,TripPaymentHead,PendingPayment
from faker import Faker

fakegen = Faker()

# @transaction.atomic
def populate_faker(N=20):
    User = get_user_model()

    # marketing_group = Group.objects.get_or_create(name='Marketing')[0]
    # sales_group = Group.objects.get_or_create(name='Sales')[0]
    # operations_group = Group.objects.get_or_create(name='Operations')[0]
    # accounts_group = Group.objects.get_or_create(name='Accounts')[0]
    # manager_group = Group.objects.get_or_create(name='Managers')[0]
    # admin_group = Group.objects.get_or_create(name='AdminUsers')[0]
    customer_group = Group.objects.get_or_create(name='Customers')[0]

    # groups = [marketing_group,sales_group,operations_group,accounts_group]
    # fields = ['Marketing','Sales','Operations','Accounts']
    #
    # for i in range(4):
    #     field = fields[i]
    #     grp = groups[i]
    #     name = field + '_manager'
    #     email= name +'@insane.travel'
    #     user = User.objects.create_user(
    #                 name = name,
    #                 email= email,
    #                 username=email,
    #                 phone=fakegen.phone_number(),
    #                 password='hdgtrkdb@75749')
    #     user.groups.add(manager_group)
    #     manager = Staff.objects.create(user=user)
    #
    #     for j in range(2):
    #         name= field + str(j)
    #         email= name+'@insane.travel'
    #         user = User.objects.create_user(
    #                     name= name,
    #                     email= email,
    #                     username=email,
    #                     phone=fakegen.phone_number(),
    #                     password='hdgtrkdb@75749')
    #         user.groups.add(grp)
    #         Staff.objects.create(user=user,manager=manager)

    for entry in range(N):
        email = fakegen.email()
        user = User.objects.create_user(
                    name=fakegen.name(),
                    email=email,
                    username=email,
                    phone=fakegen.phone_number(),
                    password='hdgtrkdb@75749')
        user.groups.add(customer_group)
        customer = Customer.objects.create(user=user)


        destination = Destination.objects.create(
                            name=fakegen.country(),
                            description= fakegen.sentence())

        vendor = Vendor.objects.create(
                            name = fakegen.company(),
                            email = fakegen.email(),
                            phone = fakegen.phone_number())
        vendor.destinations.add(destination)

        lead_source_choices = ['Friends & Family','Travel Triangle','Customer Referral','Repeat Customer','Facebook Ads','B2B','Website / Online Forums']
        lead_source = LeadSource.objects.get_or_create(name=random.choice(lead_source_choices))[0]

        staff = Staff.objects.get(id=2)
        inquiry = Inquiry.objects.create(
                                name = fakegen.name(),
                                follow_up_date = fakegen.date(),
                                remarks = fakegen.sentence(nb_words=4),
                                email = fakegen.email(),
                                phone = fakegen.phone_number(),
                                description = fakegen.sentence(nb_words=6),
                                source = lead_source,
                                id_at_source = random.randint(1111,9999),
                                status = random.choice(['NEW','ARCHIVED','LEAD']))
        inquiry.places.add(destination)
        inquiry.assigned_staff.add(staff)

        staff = Staff.objects.get(id=5)
        lead = Lead.objects.create(
                        customer=customer,
                        lead_source=lead_source,
                        id_at_lead_source=random.randint(1111,9999),
                        lead_status=random.choice(['NEW','QUOTED','BOOKED']),
                        remarks=fakegen.street_name(),
                        creation_date=fakegen.date())
        lead.destinations.add(destination)
        lead.assigned_staff.add(staff)

        staff = Staff.objects.get(id=8)
        booking = Booking.objects.create(
                        lead=lead,
                        status=random.choice(['BOOKED','TRAVELLED','CLOSED']),
                        booking_date=fakegen.date(),
                        travel_date=fakegen.date(),
                        sale_amount=random.randint(11111,99999),
                        projected_revenue=random.randint(1111,9999),
                        actual_revenue=random.randint(1111,9999),
                        tcs_amount=random.randint(111,999),
                        gst_amount=random.randint(111,999),
                        commission_paid=random.randint(111,999))
        booking.booked_destinations.add(destination)
        booking.assigned_staff.add(staff)

        account = Account.objects.get_or_create(name='HDFC')[0]

        t_head = random.choice(['Trip Payment','Bank Charges','Salary','Tech','CA & Legal','Governnment Taxes','Operational Expenses','Marketing'])
        trip_bool = True if t_head == 'Trip Payment' else False
        transaction_head = TransactionHead.objects.get_or_create(
                                    name=t_head,
                                    trip_bool=trip_bool)[0]

        tpay_head = random.choice(['Customer In-Payment','Customer Refund','Flight','Train','Hotel','Visa','Travel Insurance','Land Package','Ferry','Bus','Commission Paid','Commission Received'])
        tpay_type = 'CUSTOMER' if (tpay_head == 'Customer In-Payment' or tpay_head == 'Customer Refund') else 'VENDOR'
        trippayment_head = TripPaymentHead.objects.get_or_create(
                                    name=tpay_head,
                                    type=tpay_type)[0]

        transaction = Transaction.objects.create(
                                date = fakegen.date(),
                                account = account,
                                transaction_ref = fakegen.bban(),
                                amount = random.uniform(100,100000),
                                reference_number = fakegen.bban(),
                                description = fakegen.sentence(nb_words=4),
                                inout_type = random.choice(['DR','CR']),
                                balance = random.uniform(100,100000),
                                transaction_head = transaction_head,
                                remarks = fakegen.sentence(nb_words=4))

        for i in range(3):
            PendingPayment.objects.create(
                    date = fakegen.date(),
                    amount = random.uniform(100,100000),
                    inout_type = random.choice(['DR','CR']),
                    booking = booking)

            TripPayment.objects.create(
                date = fakegen.date(),
                amount = random.uniform(1000,10000),
                transaction = transaction,
                inout_type = random.choice(['DR','CR']),
                booking = booking,
                description = trippayment_head)


if __name__ == '__main__':
    print("Populating Script!")
    populate_faker(20)
    print("Populating Complete!")
