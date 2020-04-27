from django import forms
from django.forms import modelformset_factory

from bootstrap_modal_forms.forms import BSModalForm

from SalesApp.models import Lead,Quote,QuoteHotelInfo,QuoteTransferInfo,QuoteSightseeingInfo
from ContentApp.models import Destination,City,Hotel,Transfer,Sightseeing


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
    class Meta:
        model = Quote
        exclude = ()

    def clean(self):
        cleaned_data = super().clean()
        children = cleaned_data.get("children")
        children_age = cleaned_data.get("children_age")
        age_list = children_age_list(children_age)

        if (children and not children_age) or (children_age and not children):
            self.add_error('children',"Age of Children specified wrongly.")
        if children != 0 and children_age and (age_list == [] or len(age_list) != children):
            self.add_error('children_age',"Age of Children specified wrongly.")

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
            self.fields['cities'].queryset = self.instance.cities.all().order_by('name')

class QuoteHotelInfoForm(forms.ModelForm):
    checkin_date = forms.DateField(widget=forms.DateInput(format='%d/%m/%y'),input_formats=('%d/%m/%y', ))
    checkout_date = forms.DateField(widget=forms.DateInput(format='%d/%m/%y'),input_formats=('%d/%m/%y', ))
    price = forms.FloatField(min_value=0)
    no_of_rooms = forms.IntegerField(min_value=1,max_value=9)
    class Meta:
        model = QuoteHotelInfo
        exclude = ('quote',)

    def clean(self):
        cleaned_data = super().clean()
        city = cleaned_data.get("city")
        hotel = cleaned_data.get("hotel")
        checkin_date = cleaned_data.get('checkin_date')
        checkout_date = cleaned_data.get('checkout_date')

        if hotel and hotel.city != city:
            self.add_error('hotel',"The hotel is not present in the selected city")
        if  checkin_date and checkout_date and (checkout_date < checkin_date):
            self.add_error('checkout_date',"Check out date cannot be before check in date.")
        # if quote and (city not in quote.cities.all()):
        #     self.add_error('city',"City is not in the selected destinations.")

    # def save(self, commit=True):
    #     f = super(QuoteHotelInfoForm, self).save(commit=False)
    #     # do something here
    #     if commit:
    #         f.save()
    #     return f

    def __init__(self, *args, **kwargs):
        super(QuoteHotelInfoForm, self).__init__(*args, **kwargs)
        self.empty_permitted = True
        # self.fields['city'].queryset = City.objects.none()
        # self.fields['hotel'].queryset = Hotel.objects.none()
        if self.instance.pk:
            self.fields['city'].queryset = self.instance.quote.cities.all().order_by('destination')
            self.fields['hotel'].queryset = Hotel.objects.filter(city=self.instance.city).order_by('name')
        if self.data:
            city_ids = self.data.getlist('cities')
            self.fields['city'].queryset = City.objects.filter(pk__in=city_ids).order_by('destination')
            self.fields['hotel'].queryset = Hotel.objects.filter(city__id__in=city_ids).order_by('city')

QuoteHotelInfoFormSet = modelformset_factory(QuoteHotelInfo, form=QuoteHotelInfoForm,extra=1,can_delete=True)


class QuoteTransferInfoForm(forms.ModelForm):
    date = forms.DateField(widget=forms.DateInput(format='%d/%m/%y'),input_formats=('%d/%m/%y', ))
    class Meta:
        model = QuoteTransferInfo
        exclude = ('quote',)

    def __init__(self, *args, **kwargs):
        super(QuoteTransferInfoForm, self).__init__(*args, **kwargs)
        self.empty_permitted = True
        if self.instance.pk:
            self.fields['city'].queryset = self.instance.quote.cities.all().order_by('destination')
            self.fields['transfer'].queryset = Transfer.objects.filter(city=self.instance.city).order_by('name')
        if self.data:
            city_ids = self.data.getlist('cities')
            self.fields['city'].queryset = City.objects.filter(pk__in=city_ids).order_by('destination')
            self.fields['transfer'].queryset = Transfer.objects.filter(city__id__in=city_ids).order_by('city')

QuoteTransferInfoFormSet = modelformset_factory(QuoteTransferInfo, form=QuoteTransferInfoForm,extra=1,can_delete=True)


class QuoteSightseeingInfoForm(forms.ModelForm):
    date = forms.DateField(widget=forms.DateInput(format='%d/%m/%y'),input_formats=('%d/%m/%y', ))
    class Meta:
        model = QuoteSightseeingInfo
        exclude = ('quote',)

    def __init__(self, *args, **kwargs):
        super(QuoteSightseeingInfoForm, self).__init__(*args, **kwargs)
        self.empty_permitted = True
        if self.instance.pk:
            self.fields['city'].queryset = self.instance.quote.cities.all().order_by('destination')
            self.fields['sightseeing'].queryset = Sightseeing.objects.filter(city=self.instance.city).order_by('name')
        if self.data:
            city_ids = self.data.getlist('cities')
            self.fields['city'].queryset = City.objects.filter(pk__in=city_ids).order_by('destination')
            self.fields['sightseeing'].queryset = Sightseeing.objects.filter(city__id__in=city_ids).order_by('city')

QuoteSightseeingInfoFormSet = modelformset_factory(QuoteSightseeingInfo, form=QuoteSightseeingInfoForm,extra=1,can_delete=True)



class LeadForm(forms.ModelForm):
    class Meta:
        model = Lead
        fields = ('customer','destinations','lead_source','id_at_lead_source','lead_status','remarks')

class QuotePaxDetailForm(forms.Form):
    adults = forms.IntegerField(min_value=1)
    children = forms.IntegerField(min_value=0)
    children_age = forms.IntegerField()
    lead = forms.ModelChoiceField(queryset=Lead.objects.all(),empty_label='Select Lead')
    destinations = forms.ModelChoiceField(queryset=Destination.objects.all(),empty_label='Select Destinations')

class QuotePlacesDetailForm(forms.Form):
    start_date = forms.DateField(widget=forms.DateInput(format='%d/%m/%y'),input_formats=('%d/%m/%y', ))
    end_date = forms.DateField(widget=forms.DateInput(format='%d/%m/%y'),input_formats=('%d/%m/%y', ))
    city = forms.ModelChoiceField(queryset=City.objects.all(),empty_label='Select City')
