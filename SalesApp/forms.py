import datetime
import json

from django.db.models import F,Q
from django import forms
from django.forms import modelformset_factory, formset_factory, inlineformset_factory, BaseInlineFormSet
from django.db.models.fields import BLANK_CHOICE_DASH

from SalesApp.models import Lead,Quote, FlexInclusions, FlexItinerary, Package, Inclusion, HotelGroup
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
    discount = forms.FloatField(initial=0,required=False)
    price = forms.FloatField(required=False)
    class Meta:
        model = Quote
        fields = ('lead','title','starting_place','adults','children','children_age','start_date','end_date','destinations','cities','mark_up','discount','price')

    def clean(self):
        cleaned_data = super().clean()
        start_date = cleaned_data.get("start_date")
        end_date = cleaned_data.get("end_date")
        children = cleaned_data.get("children")
        children_age = cleaned_data.get("children_age")
        age_list = int_str_to_list(children_age)
        if (children and not children_age) or (children_age and not children):
            self.add_error('children',"Age of Children specified wrongly.")
        if children != 0 and children_age and (age_list == [] or len(age_list) != children):
            self.add_error('children_age',"Age of Children specified wrongly.")
        if start_date and end_date and start_date > end_date:
            self.add_error('end_date',"Trip end date cannot be before start date.")
        if start_date and start_date < datetime.date.today():
            self.add_error('start_date',"Trip start date cannot be in the past.")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['cities'].queryset = City.objects.none()
        if 'destinations' in self.data:
            try:
                destination_ids = self.data.getlist('destinations')
                destinations = Destination.objects.filter(pk__in=destination_ids)
                self.fields['cities'].queryset = City.objects.filter(destination__in=destinations).order_by('destination')
            except (ValueError, TypeError):
                pass  # invalid input from the user; ignore and fallback to empty City queryset
        elif self.instance.pk:
            pk = self.instance.pk
            destinations = self.instance.destinations.all()
            self.fields['cities'].queryset = City.objects.filter(destination__in=destinations).order_by('destination')

    def save(self, commit=True):
        if commit:
            f = super(QuoteForm, self).save(commit=True)
            f.inclusions_updated = False
            f.itinerary_updated = False
            f.quote_valid = False
            f.save()
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
    checkin_date = forms.DateField(widget=forms.DateInput(format='%d/%m/%y'),input_formats=('%d/%m/%y', ),required=False)
    checkout_date = forms.DateField(widget=forms.DateInput(format='%d/%m/%y'),input_formats=('%d/%m/%y', ),required=False)
    room_type = forms.CharField(initial='Standard Room',required=False)
    no_of_rooms = forms.IntegerField(min_value=1,max_value=9,initial=1,required=False)
    price = forms.FloatField(min_value=0,required=False)
    class Meta:
        model = Inclusion
        fields = ('quote','item_type','name','details','city','transports','variable_transports','hotel','transfers','sightseeings','visas','insurance','other_type',
                    'checkin_date','checkout_date','airline','room_type','no_of_rooms','price','display_order','fixed_package_item','freeze','optional','include')

    def clean(self):
        cleaned_data = super().clean()
        item_type = cleaned_data.get("item_type")
        details = cleaned_data.get("details")
        hotel = cleaned_data.get("hotel")
        transports = cleaned_data.get("transports")
        variable_transports = cleaned_data.get("variable_transports")
        city = cleaned_data.get("city")
        transfers = cleaned_data.get("transfers")
        sightseeings = cleaned_data.get("sightseeings")
        visas = cleaned_data.get("visas")
        insurance = cleaned_data.get("insurance")
        name = cleaned_data.get("name")
        price = cleaned_data.get("price")
        other_type = cleaned_data.get("other_type")
        checkin_date = cleaned_data.get("checkin_date")
        checkout_date = cleaned_data.get("checkout_date")
        airline = cleaned_data.get("airline")
        room_type = cleaned_data.get("room_type")
        no_of_rooms = cleaned_data.get("no_of_rooms")
        if item_type == 'FLIGHT':
            if not details:
                self.add_error('details',"Please enter the details.")
            if not airline:
                self.add_error('airline',"Please enter the airline name.")
            if not price:
                self.add_error('price',"Please enter the price.")
        if item_type == 'HOTEL':
            if not hotel:
                self.add_error('hotel',"Please select the hotel.")
            if not checkout_date:
                self.add_error('checkout_date',"Please enter check out date.")
            if not checkin_date:
                self.add_error('checkin_date',"Please enter check in date.")
            if not no_of_rooms:
                self.add_error('no_of_rooms',"Please enter no of rooms.")
            if not price:
                self.add_error('price',"Please enter check in price.")
            if checkin_date < self.quote.start_date or checkin_date > self.quote.end_date:
                self.add_error('checkin_date',"Check in date must be between trip start and end dates.")
        if item_type == 'TRANSPORT' and not transports:
            self.add_error('transports',"Please select the transport.")
        if item_type == 'VARIABLE_TRANSPORT':
            if not variable_transports:
                self.add_error('variable_transports',"Please select the transport.")
            if not price:
                self.add_error('price',"Please enter the price.")
        if item_type == 'TRANSFER' and not transfers:
            self.add_error('transfers',"Please select the transfers.")
        if item_type == 'SIGHTSEEING' and not sightseeings:
            self.add_error('sightseeings',"Please select the sightseeings.")
        if item_type == 'VISA' and not visas:
            self.add_error('visas',"Please select the visa.")
        if item_type == 'INSURANCE' and not insurance:
            self.add_error('insurance',"Please select the insurance.")
        if item_type == 'OTHER':
            if not name:
                self.add_error('name',"Please enter a name for inclusion.")
            if other_type in ['TRANSFER','SIGHTSEEING']:
                if not city:
                    self.add_error('city',"Please enter the city.")
                if not details:
                    self.add_error('details',"Please enter the datails.")
            if other_type == 'TRANSPORT':
                if not details:
                    self.add_error('details',"Please enter the datails.")
        if item_type == 'EXCLUSION' and not details:
            self.add_error('details',"Please enter the details.")

    def save(self, commit=True):
        f = super(QuoteInclusionForm, self).save()
        if commit:
            item_type = f.item_type
            if item_type == 'FLIGHT':
                f.display_order = 1
            elif item_type == 'HOTEL':
                f.display_order = 2
            elif item_type == 'TRANSPORT':
                f.display_order = 3
            elif item_type == 'VARIABLE_TRANSPORT':
                f.display_order = 4
            elif item_type == 'TRANSFER':
                f.display_order = 5
            elif item_type == 'SIGHTSEEING':
                f.display_order = 6
            elif item_type == 'VISA':
                f.display_order = 7
            elif item_type == 'INSURANCE':
                f.display_order = 8
            elif item_type == 'OTHER':
                f.display_order = 9
            elif item_type == 'EXCLUSION':
                f.display_order = 10
            f.save()
        return f

class QuoteInclusionInlineFormSet(BaseInlineFormSet):
    def __init__(self, *args, **kwargs):
        super(QuoteInclusionInlineFormSet, self).__init__(*args, **kwargs)
        quote = kwargs.get('instance', None)
        cities = quote.cities.all()
        hotels_qs = Hotel.objects.filter(city__in=cities)
        transfers_qs = Transfer.objects.filter(city__in=cities)
        sightseeings_qs = Sightseeing.objects.filter(city__in=cities)
        transports_qs = Transport.objects.filter(Q(from_city__in=cities) | Q(to_city__in=cities)).exclude(variable_pricing=True)
        variable_transports_qs = Transport.objects.filter(Q(from_city__in=cities) | Q(to_city__in=cities)).exclude(variable_pricing=False)
        for form in self.forms:
            form.empty_permitted = True
            form.quote = quote
            form.fields['city'].queryset = cities
            form.fields['hotel'].queryset = hotels_qs
            form.fields['transfers'].queryset = transfers_qs
            form.fields['sightseeings'].queryset = sightseeings_qs
            form.fields['transports'].queryset = transports_qs
            form.fields['variable_transports'].queryset = variable_transports_qs
QuoteInclusionFormSet = inlineformset_factory(Quote,Inclusion,form=QuoteInclusionForm,extra=3,can_delete=True,formset=QuoteInclusionInlineFormSet)


class PackageForm(forms.ModelForm):
    validity_start_date = forms.DateField(widget=forms.DateInput(format='%d/%m/%y'),input_formats=('%d/%m/%y', ),required=False)
    validity_end_date = forms.DateField(widget=forms.DateInput(format='%d/%m/%y'),input_formats=('%d/%m/%y', ),required=False)
    class Meta:
        model = Package
        fields = ('type','title','starting_place','destinations','cities','duration','price','min_pax','validity_start_date','validity_end_date')

    def save(self, commit=True):
        f = super(PackageForm, self).save()
        f.inclusions_updated = False
        f.itinerary_updated = False
        f.quote_valid = False
        f.save()
        return f

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
            form.item_type = 'HOTEL'
            form.fields['hotel'].queryset = hotels
HotelGroupFS = inlineformset_factory(HotelGroup,Inclusion,form=HotelGroupForm,extra=3,can_delete=True,formset=HotelGroupInlineFS)

class PackageInclusionForm(forms.ModelForm):
    item_type_choices = [('FLIGHT','Flight'),('TRANSPORT','Transport'),('TRANSFER','Transfer'),('SIGHTSEEING','Sightseeing'),
                            ('VISA','Visa'),('INSURANCE','Insurance'),('OTHER','Other'),('EXCLUSION','Exclusion')]
    item_type = forms.ChoiceField(choices=BLANK_CHOICE_DASH + item_type_choices,required=False)
    package = forms.ModelChoiceField(queryset=Package.objects.all(),disabled=True,required=False)

    class Meta:
        model = Inclusion
        fields = ('package','item_type','name','details','city','transports','transfers','sightseeings','visas','insurance','other_type',
                    'optional','include','display_order')

    def clean(self):
        cleaned_data = super().clean()
        item_type = cleaned_data.get("item_type")
        details = cleaned_data.get("details")
        transports = cleaned_data.get("transports")
        optional = cleaned_data.get("optional")
        city = cleaned_data.get("city")
        transfers = cleaned_data.get("transfers")
        sightseeings = cleaned_data.get("sightseeings")
        visas = cleaned_data.get("visas")
        insurance = cleaned_data.get("insurance")
        name = cleaned_data.get("name")
        other_type = cleaned_data.get("other_type")

        if item_type == 'FLIGHT' and not details:
            self.add_error('details',"Please enter the details.")
        if item_type == 'TRANSPORT' and not transports:
            self.add_error('transports',"Please select the transport.")
        if item_type == 'TRANSFER' and not transfers:
            self.add_error('transfers',"Please select the transfers.")
        if item_type == 'SIGHTSEEING' and not sightseeings:
            self.add_error('sightseeings',"Please select the sightseeings.")
        if item_type == 'VISA' and not visas:
            self.add_error('visas',"Please select the visa.")
        if item_type == 'INSURANCE' and not insurance:
            self.add_error('insurance',"Please select the insurance.")
        if item_type == 'OTHER':
            if not name:
                self.add_error('name',"Please enter a name for inclusion.")
            if other_type in ['TRANSFER','SIGHTSEEING']:
                if not city:
                    self.add_error('city',"Please enter the city.")
                if not details:
                    self.add_error('details',"Please enter the datails.")
            if other_type == 'TRANSPORT':
                if not details:
                    self.add_error('details',"Please enter the datails.")
        if item_type == 'EXCLUSION' and not details:
            self.add_error('details',"Please enter the details.")

    def save(self, commit=True):
        f = super(PackageInclusionForm, self).save()
        if commit:
            item_type = f.item_type
            if item_type == 'FLIGHT':
                f.display_order = 1
            elif item_type == 'TRANSPORT':
                f.display_order = 3
            elif item_type == 'TRANSFER':
                f.display_order = 5
            elif item_type == 'SIGHTSEEING':
                f.display_order = 6
            elif item_type == 'VISA':
                f.display_order = 7
            elif item_type == 'INSURANCE':
                f.display_order = 8
            elif item_type == 'OTHER':
                f.display_order = 9
            elif item_type == 'EXCLUSION':
                f.display_order = 10
            f.save()
        return f

class PackageInclusionInlineFormSet(BaseInlineFormSet):
    def __init__(self, *args, **kwargs):
        super(PackageInclusionInlineFormSet, self).__init__(*args, **kwargs)
        package = kwargs.get('instance', None)
        cities = package.cities.all()
        transfers = Transfer.objects.filter(city__in=cities)
        sightseeings = Sightseeing.objects.filter(city__in=cities)
        transports = Transport.objects.filter(Q(from_city__in=cities) | Q(to_city__in=cities))
        for form in self.forms:
            form.empty_permitted = True
            form.fields['city'].queryset = cities
            form.fields['transfers'].queryset = transfers
            form.fields['sightseeings'].queryset = sightseeings
            form.fields['transports'].queryset = transports

PackageInclusionFormSet = inlineformset_factory(Package,Inclusion,form=PackageInclusionForm,extra=3,can_delete=True,formset=PackageInclusionInlineFormSet)


class ItineraryForm(forms.Form):
    itinerary = forms.CharField(required=False)
    def __init__(self, *args, **kwargs):
        super(ItineraryForm, self).__init__(*args, **kwargs)
        self.empty_permitted = True
ItineraryFormSet = formset_factory(form=ItineraryForm,extra=0)


class FlexInclusionsForm(forms.ModelForm):
    class Meta:
        model = FlexInclusions
        exclude = ()
    def save(self, commit=True):
        f = super(FlexInclusionsForm, self).save(commit=False)
        if commit:
            quote = f.quote
            quote.quote_inclusions = True
            quote.inclusions_updated = True
            quote.inclusions_format = 'FLEXIBLE'
            quote.itinerary_updated = False
            quote.quote_valid = False
            quote.save()
            f.save()
        return f

class FlexItineraryForm(forms.ModelForm):
    quote = forms.ModelChoiceField(queryset=Quote.objects.all(),disabled=True,required=False)
    # content = forms.CharField(widget=TinyMCE(attrs={'cols': 80, 'rows': 30}))
    class Meta:
        model = FlexItinerary
        exclude = ()
    def save(self, commit=True):
        f = super(FlexItineraryForm, self).save(commit=False)
        if commit:
            quote = f.quote
            quote.quote_itinerary = True
            if quote.inclusions_updated:
                quote.itinerary_updated = True
                quote.quote_valid = True
            quote.save()
            f.save()
        return f


class LeadForm(forms.ModelForm):
    class Meta:
        model = Lead
        fields = ('customer','destinations','lead_source','id_at_lead_source','lead_status','remarks')
