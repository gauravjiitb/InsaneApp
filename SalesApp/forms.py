from datetime import datetime

from django import forms
from django.forms import modelformset_factory

from bootstrap_modal_forms.forms import BSModalForm

from SalesApp.models import (Lead,Quote,QuoteFlightInfo,
                                        QuoteTransportInfo,
                                        QuoteHotelInfo,
                                        QuoteTransferInfo,
                                        QuoteSightseeingInfo,
                                        QuoteVisaInfo,
                                        QuoteInsuranceInfo,
                                        QuoteItineraryInfo,
                                        QuoteOthersInfo)
from SalesApp.models import FlexInclusions,FlexItinerary
from ContentApp.models import Destination,City,Hotel,Transfer,Sightseeing,Visa,Insurance


###############################################################################
#
def children_age_list(age_string):
    try:
        age_list = list(age_string.split(","))
        for i in range(len(age_list)):
            age_list[i] = int(age_list[i])
            if age_list[i] < 0:
                return []
    except:
        age_list = []
    return age_list

###############################################################################
class QuoteForm(forms.ModelForm):
    start_date = forms.DateField(widget=forms.DateInput(format='%d/%m/%y'),input_formats=('%d/%m/%y', ))
    end_date = forms.DateField(widget=forms.DateInput(format='%d/%m/%y'),input_formats=('%d/%m/%y', ))
    price = forms.FloatField(disabled=True,required=False)
    class Meta:
        model = Quote
        exclude = ('quote_active','inclusions_format','quote_inclusions','quote_itinerary','inclusions_updated','itinerary_updated','quote_valid')

    def clean(self):
        cleaned_data = super().clean()
        start_date = cleaned_data.get("start_date")
        end_date = cleaned_data.get("end_date")
        children = cleaned_data.get("children")
        children_age = cleaned_data.get("children_age")
        age_list = children_age_list(children_age)
        if (children and not children_age) or (children_age and not children):
            self.add_error('children',"Age of Children specified wrongly.")
        if children != 0 and children_age and (age_list == [] or len(age_list) != children):
            self.add_error('children_age',"Age of Children specified wrongly.")
        if start_date and end_date and start_date > end_date:
            self.add_error('end_date',"Trip end date cannot be before start date.")
        # if start_date and start_date < datetime.today():
        #     self.add_error('start_date',"Trip start date cannot be in the past.")

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
            self.fields['cities'].queryset = self.instance.cities.all().order_by('destination')

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

class QuoteFlightInfoForm(forms.ModelForm):
    quote = forms.ModelChoiceField(queryset=Quote.objects.all(),disabled=True,required=False)
    price = forms.FloatField(min_value=0)
    class Meta:
        model = QuoteFlightInfo
        exclude = ()
    def __init__(self, *args, **kwargs):
        super(QuoteFlightInfoForm, self).__init__(*args, **kwargs)
        self.empty_permitted = True
QuoteFlightInfoFormSet = modelformset_factory(QuoteFlightInfo, form=QuoteFlightInfoForm, extra=0,can_delete=True)

class QuoteTransportInfoForm(forms.ModelForm):
    quote = forms.ModelChoiceField(queryset=Quote.objects.all(),disabled=True,required=False)
    date = forms.DateField(widget=forms.DateInput(format='%d/%m/%y'),input_formats=('%d/%m/%y', ))
    price = forms.FloatField(min_value=0)
    class Meta:
        model = QuoteTransportInfo
        exclude = ()
    def clean(self):
        cleaned_data = super().clean()
        date = cleaned_data.get("date")
        quote = cleaned_data.get('quote')
        if quote and date and (date < quote.start_date or date > quote.end_date):
            self.add_error('date',"Date must be between trip start date and end date.")
    def __init__(self, *args, **kwargs):
        super(QuoteTransportInfoForm, self).__init__(*args, **kwargs)
        self.empty_permitted = True
QuoteTransportInfoFormSet = modelformset_factory(QuoteTransportInfo, form=QuoteTransportInfoForm, extra=1,can_delete=True)

class QuoteHotelInfoForm(forms.ModelForm):
    quote = forms.ModelChoiceField(queryset=Quote.objects.all(),disabled=True,required=False)
    checkin_date = forms.DateField(widget=forms.DateInput(format='%d/%m/%y'),input_formats=('%d/%m/%y', ))
    checkout_date = forms.DateField(widget=forms.DateInput(format='%d/%m/%y'),input_formats=('%d/%m/%y', ))
    room_type = forms.CharField(initial='Standard Room',required=False)
    no_of_rooms = forms.IntegerField(min_value=1,max_value=9,initial=1)
    price = forms.FloatField(min_value=0)
    class Meta:
        model = QuoteHotelInfo
        exclude = ()
    def clean(self):
        cleaned_data = super().clean()
        city = cleaned_data.get("city")
        hotel = cleaned_data.get("hotel")
        checkin_date = cleaned_data.get('checkin_date')
        checkout_date = cleaned_data.get('checkout_date')
        quote = cleaned_data.get('quote')
        if hotel and city and hotel.city != city:
            self.add_error('hotel',"The hotel is not present in the selected city")
        if  checkin_date and checkout_date and (checkout_date < checkin_date):
            self.add_error('checkout_date',"Check out date cannot be before check in date.")
        if checkin_date and quote and (checkin_date < quote.start_date or checkin_date > quote.end_date):
            self.add_error('checkin_date',"Check in date must be between trip start date and end date.")
        if checkout_date and quote and (checkout_date < quote.start_date or checkout_date > quote.end_date):
            self.add_error('checkout_date',"Check out date must be between trip start date and end date.")
    def __init__(self, *args, **kwargs):
        super(QuoteHotelInfoForm, self).__init__(*args, **kwargs)
        self.empty_permitted = True
        if self.instance.pk:
            self.fields['city'].queryset = self.instance.quote.cities.all().order_by('destination')
            self.fields['hotel'].queryset = Hotel.objects.filter(city=self.instance.city).order_by('name')
        # elif self.data:
        #     city_ids = self.data.getlist('cities')
        #     self.fields['city'].queryset = City.objects.filter(pk__in=city_ids).order_by('destination')
        #     self.fields['hotel'].queryset = Hotel.objects.filter(city__id__in=city_ids).order_by('city')
        else:
            quote = kwargs.get('initial', None).get('quote',None)
            self.fields['city'].queryset = quote.cities.all().order_by('destination')
            self.fields['hotel'].queryset = Hotel.objects.filter(city__in=quote.cities.all())
QuoteHotelInfoFormSet = modelformset_factory(QuoteHotelInfo, form=QuoteHotelInfoForm,extra=1,can_delete=True)


class QuoteTransferInfoForm(forms.ModelForm):
    quote = forms.ModelChoiceField(queryset=Quote.objects.all(),disabled=True,required=False)
    transfer = forms.ModelChoiceField(queryset=Transfer.objects.filter(price__gt=0))
    date = forms.DateField(widget=forms.DateInput(format='%d/%m/%y'),input_formats=('%d/%m/%y', ))
    class Meta:
        model = QuoteTransferInfo
        exclude = ()
    def clean(self):
        cleaned_data = super().clean()
        date = cleaned_data.get("date")
        quote = cleaned_data.get('quote')
        city = cleaned_data.get("city")
        transfer = cleaned_data.get('transfer')
        if quote and date and (date < quote.start_date or date > quote.end_date):
            self.add_error('date',"Date must be between trip start date and end date.")
        if transfer and city and transfer.city != city:
            self.add_error('transfer',"This transfer is not present in the selected city")
    def __init__(self, *args, **kwargs):
        super(QuoteTransferInfoForm, self).__init__(*args, **kwargs)
        self.empty_permitted = True
        if self.instance.pk:
            self.fields['city'].queryset = self.instance.quote.cities.all().order_by('destination')
            self.fields['transfer'].queryset = Transfer.objects.filter(city=self.instance.city,price__gt=0)
        else:
            quote = kwargs.get('initial', None).get('quote',None)
            self.fields['city'].queryset = quote.cities.all().order_by('destination')
            self.fields['transfer'].queryset = Transfer.objects.filter(city__in=quote.cities.all(),price__gt=0)
QuoteTransferInfoFormSet = modelformset_factory(QuoteTransferInfo, form=QuoteTransferInfoForm,extra=1,can_delete=True)


class QuoteSightseeingInfoForm(forms.ModelForm):
    quote = forms.ModelChoiceField(queryset=Quote.objects.all(),disabled=True,required=False)
    sightseeing = forms.ModelChoiceField(queryset=Sightseeing.objects.filter(adult_price__gt=0,child_price__gt=0))
    date = forms.DateField(widget=forms.DateInput(format='%d/%m/%y'),input_formats=('%d/%m/%y', ))
    class Meta:
        model = QuoteSightseeingInfo
        exclude = ()
    def clean(self):
        cleaned_data = super().clean()
        date = cleaned_data.get("date")
        quote = cleaned_data.get('quote')
        city = cleaned_data.get("city")
        sightseeing = cleaned_data.get('sightseeing')
        if quote and date and (date < quote.start_date or date > quote.end_date):
            self.add_error('date',"Date must be between trip start date and end date.")
        if sightseeing and city and sightseeing.city != city:
            self.add_error('sightseeing',"This sightseeing tour is not present in the selected city")
    def __init__(self, *args, **kwargs):
        super(QuoteSightseeingInfoForm, self).__init__(*args, **kwargs)
        self.empty_permitted = True
        if self.instance.pk:
            self.fields['city'].queryset = self.instance.quote.cities.all().order_by('destination')
            self.fields['sightseeing'].queryset = Sightseeing.objects.filter(city=self.instance.city,adult_price__gt=0,child_price__gt=0).order_by('name')
        else:
            quote = kwargs.get('initial', None).get('quote',None)
            self.fields['city'].queryset = quote.cities.all().order_by('destination')
            self.fields['sightseeing'].queryset = Sightseeing.objects.filter(city__in=quote.cities.all(),adult_price__gt=0,child_price__gt=0).order_by('name')
QuoteSightseeingInfoFormSet = modelformset_factory(QuoteSightseeingInfo, form=QuoteSightseeingInfoForm,extra=1,can_delete=True)


class QuoteVisaInfoForm(forms.ModelForm):
    quote = forms.ModelChoiceField(queryset=Quote.objects.all(),disabled=True,required=False)
    class Meta:
        model = QuoteSightseeingInfo
        exclude = ()
    def __init__(self, *args, **kwargs):
        super(QuoteVisaInfoForm, self).__init__(*args, **kwargs)
        self.empty_permitted = True
QuoteVisaInfoFormSet = modelformset_factory(QuoteVisaInfo, form=QuoteVisaInfoForm,extra=1,can_delete=True)

class QuoteInsuranceInfoForm(forms.ModelForm):
    quote = forms.ModelChoiceField(queryset=Quote.objects.all(),disabled=True,required=False)
    class Meta:
        model = QuoteInsuranceInfo
        exclude = ()
    def __init__(self, *args, **kwargs):
        super(QuoteInsuranceInfoForm, self).__init__(*args, **kwargs)
        self.empty_permitted = True
QuoteInsuranceInfoFormSet = modelformset_factory(QuoteInsuranceInfo, form=QuoteInsuranceInfoForm,extra=1,can_delete=True)

class QuoteOthersInfoForm(forms.ModelForm):
    quote = forms.ModelChoiceField(queryset=Quote.objects.all(),disabled=True,required=False)
    date = forms.DateField(widget=forms.DateInput(format='%d/%m/%y'),input_formats=('%d/%m/%y', ),required=False)
    price = forms.FloatField(min_value=0,required=False)
    class Meta:
        model = QuoteOthersInfo
        exclude = ()
    def clean(self):
        cleaned_data = super().clean()
        date = cleaned_data.get("date")
        quote = cleaned_data.get('quote')
        city = cleaned_data.get("city")
        type = cleaned_data.get("type")
        description = cleaned_data.get("description")
        if date and (date < quote.start_date or date > quote.end_date):
            self.add_error('date',"Date must be between trip start date and end date.")
        if (type == 'TRANSFER' or type == 'SIGHTSEEING'):
            if not city:
                self.add_error('city',"City must be specified for transfers or sightseeing.")
            if not description:
                self.add_error('description',"Description must be specified for transfers or sightseeing.")
            if not date:
                self.add_error('date',"Date must be specified for transfers or sightseeing.")
    def __init__(self, *args, **kwargs):
        super(QuoteOthersInfoForm, self).__init__(*args, **kwargs)
        self.empty_permitted = True
        if self.instance.pk:
            self.fields['city'].queryset = self.instance.quote.cities.all().order_by('destination')
        else:
            quote = kwargs.get('initial', None).get('quote',None)
            self.fields['city'].queryset = quote.cities.all().order_by('destination')
QuoteOthersInfoFormSet = modelformset_factory(QuoteOthersInfo, form=QuoteOthersInfoForm, extra=1,can_delete=True)

class QuoteItineraryInfoForm(forms.ModelForm):
    quote = forms.ModelChoiceField(queryset=Quote.objects.all(),disabled=True,required=False)
    class Meta:
        model = QuoteItineraryInfo
        exclude = ('description',)
    def __init__(self, *args, **kwargs):
        super(QuoteItineraryInfoForm, self).__init__(*args, **kwargs)
        self.empty_permitted = True
QuoteItineraryInfoFormSet = modelformset_factory(QuoteItineraryInfo, form=QuoteItineraryInfoForm,extra=0)


class LeadForm(forms.ModelForm):
    class Meta:
        model = Lead
        fields = ('customer','destinations','lead_source','id_at_lead_source','lead_status','remarks')

# class QuotePaxDetailForm(forms.Form):
#     adults = forms.IntegerField(min_value=1)
#     children = forms.IntegerField(min_value=0)
#     children_age = forms.IntegerField()
#     lead = forms.ModelChoiceField(queryset=Lead.objects.all(),empty_label='Select Lead')
#     destinations = forms.ModelChoiceField(queryset=Destination.objects.all(),empty_label='Select Destinations')
#
# class QuotePlacesDetailForm(forms.Form):
#     start_date = forms.DateField(widget=forms.DateInput(format='%d/%m/%y'),input_formats=('%d/%m/%y', ))
#     end_date = forms.DateField(widget=forms.DateInput(format='%d/%m/%y'),input_formats=('%d/%m/%y', ))
#     city = forms.ModelChoiceField(queryset=City.objects.all(),empty_label='Select City')
