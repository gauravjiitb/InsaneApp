import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE','InsaneDjangoApp.settings')

import django
django.setup()

import random
from django.contrib.auth import get_user_model
from django.db import transaction
from django.contrib.auth.models import Group, Permission

from ContentApp.models import Destination, Vendor,City, Hotel, Transfer, Sightseeing
from MarketingApp.models import LeadSource,Inquiry
from ProfilesApp.models import Customer,Staff
from SalesApp.models import Lead
from OperationsApp.models import Booking
from AccountsApp.models import Account,Transaction,TransactionHead,TripPayment,TripPaymentHead,PendingPayment
from faker import Faker

fakegen = Faker()

@transaction.atomic
def populate_groups_staff():
    User = get_user_model()
    marketing_group = Group.objects.get_or_create(name='Marketing')[0]
    sales_group = Group.objects.get_or_create(name='Sales')[0]
    operations_group = Group.objects.get_or_create(name='Operations')[0]
    accounts_group = Group.objects.get_or_create(name='Accounts')[0]
    manager_group = Group.objects.get_or_create(name='Managers')[0]
    admin_group = Group.objects.get_or_create(name='AdminUsers')[0]
    customer_group = Group.objects.get_or_create(name='Customers')[0]

    groups = [marketing_group,sales_group,operations_group,accounts_group]
    fields = ['Marketing','Sales','Operations','Accounts']

    admin_user = User.objects.create_user(
                            name = 'AdminUser',
                            email = "adminuser@insane.travel",
                            username = "adminuser@insane.travel",
                            phone = fakegen.phone_number(),
                            password='hdgtrkdb@75749')
    admin_staff = Staff.objects.create(user=admin_user,manager=Staff.objects.get(user__name='admin'))

    for i in range(4):
        field = fields[i]
        grp = groups[i]
        name = field + '_manager'
        email= name +'@insane.travel'
        user = User.objects.create_user(
                    name = name,
                    email= email,
                    username=email,
                    phone=fakegen.phone_number(),
                    password='hdgtrkdb@75749')
        user.groups.add(manager_group)
        manager = Staff.objects.create(user=user,manager=admin_staff)

        name= field + '_user'
        email= name+'@insane.travel'
        user = User.objects.create_user(
                    name= name,
                    email= email,
                    username=email,
                    phone=fakegen.phone_number(),
                    password='hdgtrkdb@75749')
        user.groups.add(grp)
        Staff.objects.create(user=user,manager=manager)
        print('Staff Users Created')


@transaction.atomic
def populate_customers(N=20):
    User = get_user_model()
    customer_group = Group.objects.get(name='Customers')
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
    print('Customers Created')


@transaction.atomic
def populate_destinations_vendors_cities(N=20):
    for i in range(N):
        destination = Destination.objects.create(
                            name=fakegen.country(),
                            description= fakegen.sentence())
        vendor = Vendor.objects.create(
                            name = fakegen.company(),
                            email = fakegen.email(),
                            phone = fakegen.phone_number())
        vendor.destinations.add(destination)

        City.objects.create(
                        name = fakegen.city(),
                        destination = destination)
    print('Destinations, Cities and Vendors Created')

@transaction.atomic
def populate_hotels_transfers_sightseeings(N=20):
    transfer_type_choices = ['PRIVATE','SHARED']
    for i in range(N):
        x = random.randint(1,20)
        cityname = City.objects.get(id=x)

        Hotel.objects.create(
            name = fakegen.city() + " Hotel",
            city = cityname,
            email = fakegen.email(),
            phone = fakegen.phone_number())
        Transfer.objects.create(
            city = cityname,
            name = fakegen.city()+" Airport to Hotel",
            transfer_type = random.choice(transfer_type_choices),
            description = fakegen.sentence(),
            max_pax = random.randint(2,6),
            price = random.randint(1000,2500))
        Sightseeing.objects.create(
            city = cityname,
            name = fakegen.city() + " Day Tour",
            description = fakegen.sentence(),
            adult_price = random.randint(2000,6000),
            child_price = random.randint(1500,2000),
            duration = random.randint(2,10),
            remarks = fakegen.sentence())


@transaction.atomic
def populate_leadsource_inquiries(N=20):
    User = get_user_model()
    for i in range(N):
        lead_source_choices = ['Friends & Family','Travel Triangle','Customer Referral','Repeat Customer','Facebook Ads','B2B','Website / Online Forums']
        lead_source = LeadSource.objects.get_or_create(name=random.choice(lead_source_choices))[0]

        staff = Staff.objects.get(user__name='Marketing_user')
        index = random.randint(1,N)
        destination = Destination.objects.get(id=index)

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
    print('Lead Sources and Inquiries Created')


# @transaction.atomic
def populates_leads_bookings(N=20):
    User = get_user_model()
    lead_source_choices = ['Friends & Family','Travel Triangle','Customer Referral','Repeat Customer','Facebook Ads','B2B','Website / Online Forums']

    for i in range(N):
        staff = Staff.objects.get(user__name='Sales_user')
        index = random.randint(1,N)
        destination = Destination.objects.get(id=index)
        lead_source = LeadSource.objects.get(name=random.choice(lead_source_choices))
        customer = Customer.objects.get(id=index)
        lead = Lead.objects.create(
                        customer=customer,
                        lead_source=lead_source,
                        id_at_lead_source=random.randint(1111,9999),
                        lead_status=random.choice(['NEW','QUOTED','BOOKED']),
                        remarks=fakegen.street_name(),
                        creation_date=fakegen.date())
        lead.destinations.add(destination)
        lead.assigned_staff.add(staff)

        staff = Staff.objects.get(user__name='Operations_user')
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
    print('Leads and Bookings Created.')


@transaction.atomic
def populate_accounts_data(N=20):
    User = get_user_model()
    account = Account.objects.create(name='HDFC')

    for i in range(N):
        index = random.randint(1,N)
        booking = Booking.objects.get(id=index)

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

        for j in range(3):
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
    print('Accounts, TransactionHeads, TripPaymentHeads, Transactions, PendingPayments, TripPayments Created')

if __name__ == '__main__':
    print("Populating Script!")
    # populate_groups_staff()
    # populate_customers()
    # populate_destinations_vendors_cities()
    # populate_hotels_transfers_sightseeings(40)
    # populate_leadsource_inquiries()
    # populates_leads_bookings()
    # populate_accounts_data()
    print("Populating Complete!")
