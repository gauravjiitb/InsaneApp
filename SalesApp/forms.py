import datetime
import json

from django.db.models import F,Q
from django import forms
from django.forms import modelformset_factory, formset_factory, inlineformset_factory, BaseInlineFormSet
from django.db.models.fields import BLANK_CHOICE_DASH

from SalesApp.models import Lead,Quote, Package, Inclusion, HotelGroup
from ContentApp.models import Destination,City,Hotel,Transfer,Sightseeing,Visa,Insurance,Transport


###############################################################################
# UTILITY FUNCTIONS
###############################################################################
def int_str_to_list(int_string):
    """ Takes a list of positive integers and returns a list. If improper format, returns empty list"""
    try:
        int_list = list(int_string.split(","))
        for i in range(len(int_list)):
            int_list[i] = int(int_list[i])
            if int_list[i] < 0:
                return []
    except:
        int_list = []
    return int_list

###############################################################################

class QuoteForm(forms.ModelForm):
    start_date = forms.DateField(widget=forms.DateInput(format='%d/%m/%y'),input_formats=('%d/%m/%y', ))
    end_date = forms.DateField(widget=forms.DateInput(format='%d/%m/%y'),input_formats=('%d/%m/%y', ))

    class Meta:
        model = Quote
        fields = ('lead','themes','tags','title','starting_place','adults','children','children_age','start_date','end_date','destinations','cities')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['cities'].queryset = City.objects.none()
        if 'destinations' in self.data:
            destination_ids = self.data.getlist('destinations')
            destinations = Destination.objects.filter(pk__in=destination_ids)
            self.fields['cities'].queryset = City.objects.filter(destination__in=destinations).order_by('destination')
        elif self.instance.pk:
            pk = self.instance.pk
            destinations = self.instance.destinations.all()
            self.fields['cities'].queryset = City.objects.filter(destination__in=destinations).order_by('destination')

    def save(self, commit=True):
        if commit:
            f = super(QuoteForm, self).save(commit=True)
            f.duration = (f.end_date - f.start_date).days + 1
            f.inclusions_updated = False
            f.itinerary_updated = False
            f.price_valid = False
            f.quote_valid = False
            f.save()
            lead = f.lead
            lead.lead_status = 'QUOTED'
            lead.save()
        else:
            f = super(QuoteForm, self).save(commit=False)
        return f


class QuotePackagesSelectForm(forms.Form):
    package1 = forms.ModelChoiceField(queryset=Package.objects.all(),required=False)
    package2 = forms.ModelChoiceField(queryset=Package.objects.all(),required=False)
    package3 = forms.ModelChoiceField(queryset=Package.objects.all(),required=False)
    order1 = forms.IntegerField(initial=1,min_value=1,max_value=3,required=False,disabled=True)
    order2 = forms.IntegerField(initial=2,min_value=1,max_value=3,required=False,disabled=True)
    order3 = forms.IntegerField(initial=3,min_value=1,max_value=3,required=False,disabled=True)
    hotel_group1 = forms.ModelChoiceField(queryset=HotelGroup.objects.all(),required=False)
    hotel_group2 = forms.ModelChoiceField(queryset=HotelGroup.objects.all(),required=False)
    hotel_group3 = forms.ModelChoiceField(queryset=HotelGroup.objects.all(),required=False)
    # def __init__(self, *args, **kwargs):
    #     super().__init__(*args, **kwargs)
    #     self.fields['packages'].queryset = Package.objects.filter(destinations__in=quote.destinations.all())


class QuoteInclusionForm(forms.ModelForm):
    quote = forms.ModelChoiceField(queryset=Quote.objects.all(),disabled=True,required=False)
    room_type = forms.CharField(initial='Standard Room',required=False)
    price = forms.FloatField(min_value=0,required=False)
    class Meta:
        model = Inclusion
        fields = ('title','quote','item_type','name','details','city','transport','hotel','transfer','sightseeing','visa','insurance','other_type',
                    'day','nights','airline','room_type','price','freeze','optional','include','itinerary_inclusion')
    def save(self, commit=True):
        if commit:
            f = super(QuoteInclusionForm, self).save(commit=True)
            if f.item_type == '0_FLIGHT':
                f.title = '{}: \n{}'.format(f.airline, f.details)
            elif f.item_type == '1_HOTEL':
                f.title = '{} Nights | {} | {}'.format(f.nights, f.hotel, f.room_type)
            elif f.item_type == '2_TRANSPORT':
                f.title = '{}'.format(f.transport)
            elif f.item_type == '3_TRANSFER':
                f.title = '{}'.format(f.transfer)
            elif f.item_type == '4_SIGHTSEEING':
                f.title = '{}'.format(f.sightseeing)
            elif f.item_type == '5_VISA':
                f.title = '{}'.format(f.visa)
            elif f.item_type == '6_INSURANCE':
                f.title = '{}'.format(f.insurance)
            elif f.item_type == '7_OTHER':
                f.title = f.name
            elif f.item_type == '8_EXCLUSION':
                f.title = f.details
            f.save()
        else:
            f = super(QuoteInclusionForm, self).save(commit=False)
        return f

class QuoteInclusionInlineFS(BaseInlineFormSet):
    def __init__(self, *args, **kwargs):
        super(QuoteInclusionInlineFS, self).__init__(*args, **kwargs)
        quote = kwargs.get('instance', None)
        cities = quote.cities.all()
        hotels_qs = Hotel.objects.filter(city__in=cities)
        transfers_qs = Transfer.objects.filter(city__in=cities)
        sightseeings_qs = Sightseeing.objects.filter(city__in=cities)
        transports_qs = Transport.objects.filter(Q(from_city__in=cities) | Q(to_city__in=cities))
        for form in self.forms:
            form.empty_permitted = True
            form.quote = quote
            form.fields['city'].queryset = cities
            form.fields['hotel'].queryset = hotels_qs
            form.fields['transfer'].queryset = transfers_qs
            form.fields['sightseeing'].queryset = sightseeings_qs
            form.fields['transport'].queryset = transports_qs
QuoteInclusionFS = inlineformset_factory(Quote,Inclusion,form=QuoteInclusionForm,extra=3,can_delete=True,formset=QuoteInclusionInlineFS)

class InclusionBulkSelectForm(forms.Form):
    transports = forms.ModelMultipleChoiceField(queryset=Transport.objects.all(),required=False)
    transfers = forms.ModelMultipleChoiceField(queryset=Transfer.objects.all(),required=False)
    sightseeings = forms.ModelMultipleChoiceField(queryset=Sightseeing.objects.all(),required=False)
    visas = forms.ModelMultipleChoiceField(queryset=Visa.objects.all(),required=False)
    def __init__(self, *args, **kwargs):
        object = kwargs.pop('object', None)
        super(InclusionBulkSelectForm, self).__init__(*args, **kwargs)
        cities = object.cities.all()
        transfers_qs = Transfer.objects.filter(city__in=cities)
        sightseeings_qs = Sightseeing.objects.filter(city__in=cities)
        transports_qs = Transport.objects.filter(Q(from_city__in=cities) | Q(to_city__in=cities))
        self.fields['transports'].queryset = transports_qs
        self.fields['transfers'].queryset = transfers_qs
        self.fields['sightseeings'].queryset = sightseeings_qs



class PackageForm(forms.ModelForm):
    validity_start_date = forms.DateField(widget=forms.DateInput(format='%d/%m/%y'),input_formats=('%d/%m/%y', ),required=False)
    validity_end_date = forms.DateField(widget=forms.DateInput(format='%d/%m/%y'),input_formats=('%d/%m/%y', ),required=False)
    class Meta:
        model = Package
        fields = ('type','themes','tags','title','starting_place','destinations','cities','duration','price','min_pax','validity_start_date','validity_end_date')


class PackageInclusionForm(forms.ModelForm):
    package = forms.ModelChoiceField(queryset=Package.objects.all(),disabled=True,required=False)
    item_type_choices = [('0_FLIGHT','Flight'),('2_TRANSPORT','Transport'),('3_TRANSFER','Transfer'),('4_SIGHTSEEING','Sightseeing'),
                            ('5_VISA','Visa'),('6_INSURANCE','Insurance'),('7_OTHER','Other'),('8_EXCLUSION','Exclusion')]
    item_type = forms.ChoiceField(choices=BLANK_CHOICE_DASH + item_type_choices,required=False)
    class Meta:
        model = Inclusion
        fields = ('title','package','item_type','name','details','city','transport','transfer','sightseeing','visa','insurance','other_type',
                    'day','nights','optional','include','itinerary_inclusion')
    def save(self, commit=True):
        if commit:
            f = super(PackageInclusionForm, self).save(commit=True)
            if f.item_type == '0_FLIGHT':
                f.title = 'Flight | {}'.format(f.airline)
            elif f.item_type == '2_TRANSPORT':
                f.title = '{}'.format(f.transport)
            elif f.item_type == '3_TRANSFER':
                f.title = '{}'.format(f.transfer)
            elif f.item_type == '4_SIGHTSEEING':
                f.title = '{}'.format(f.sightseeing)
            elif f.item_type == '5_VISA':
                f.title = '{}'.format(f.visa)
            elif f.item_type == '6_INSURANCE':
                f.title = '{}'.format(f.insurance)
            elif f.item_type == '7_OTHER':
                f.title = self.name
            f.save()
        else:
            f = super(PackageInclusionForm, self).save(commit=False)
        return f

class PackageInclusionInlineFS(BaseInlineFormSet):
    def __init__(self, *args, **kwargs):
        super(PackageInclusionInlineFS, self).__init__(*args, **kwargs)
        package = kwargs.get('instance', None)
        cities = package.cities.all()
        transfers_qs = Transfer.objects.filter(city__in=cities)
        sightseeings_qs = Sightseeing.objects.filter(city__in=cities)
        transports_qs = Transport.objects.filter(Q(from_city__in=cities) | Q(to_city__in=cities))
        for form in self.forms:
            form.empty_permitted = True
            form.package = package
            form.fields['city'].queryset = cities
            form.fields['transfer'].queryset = transfers_qs
            form.fields['sightseeing'].queryset = sightseeings_qs
            form.fields['transport'].queryset = transports_qs
PackageInclusionFS = inlineformset_factory(Package,Inclusion,form=PackageInclusionForm,extra=3,can_delete=True,formset=PackageInclusionInlineFS)


class HotelGroupForm(forms.ModelForm):
    class Meta:
        model = Inclusion
        fields = ('item_type','nights','hotel','room_type')

class HotelGroupInlineFS(BaseInlineFormSet):
    def __init__(self, *args, **kwargs):
        super(HotelGroupInlineFS, self).__init__(*args, **kwargs)
        hotel_group = kwargs.get('instance', None)
        cities = hotel_group.package.cities.all()
        hotels = Hotel.objects.filter(city__in=cities)
        for form in self.forms:
            form.empty_permitted = True
            form.item_type = '2_HOTEL'
            form.fields['hotel'].queryset = hotels
HotelGroupFS = inlineformset_factory(HotelGroup,Inclusion,form=HotelGroupForm,extra=3,can_delete=True,formset=HotelGroupInlineFS)



class LeadForm(forms.ModelForm):
    class Meta:
        model = Lead
        fields = ('customer','destinations','lead_source','id_at_lead_source','lead_status','remarks')
