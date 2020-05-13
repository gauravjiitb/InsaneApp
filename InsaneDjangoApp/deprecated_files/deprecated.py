##########################################################################
#   JAVASCRIPT CODE
##########################################################################

# SCRIPT FOR RENDERING CHILDREN AGE FIELDS
# $("label[for*='children_age']").parent().hide();
# $("input#id_children").on('change',function(){
#   var n = $(this).val();
#
#   if (n == 0) {
#     template = "<label for='id_children_age'></label>";
#     $("label[for*='children_age']").parent().hide();
#   } else{
#     template = "<label for='id_children_age'>Children age</label>";
#     for(var i = 0; i < n; i++){
#       template += `<input type="number" name="children_age" placeholder="Children ${i+1} age" class="form-control" required="" id="id_children_${i}_age" >`;
#     }
#
#   }
#   $("label[for*='children_age']").parent().html(template);
#   $("label[for*='children_age']").parent().show();
# });



# // SCRIPT FOR VARYING CITY SELECTION IN QUOTE INFO BASED ON DESTINATIONS SELECTED
# $("#id_destinations").change(function () {
#   var url = $("#quoteForm").attr("data-cities-url");  // get the url of the `quote_load_cities` view
#   var destination_ids = $(this).val();  // get the selected country ID from the HTML input
#
#   $.ajax({                       // initialize an AJAX request
#     url: url,                    // set the url of the request (= localhost:8000/sales/ajax/quote/load-cities/)
#     data: {
#       'destinations': destination_ids       // add the destination id to the GET parameters
#     },
#     success: function (data) {   // `data` is the return of the `load_cities` view function
#       $("#id_cities").html(data);  // replace the contents of the city input with the data that came from the server
#     }
#   });
# });



# // SCRIPT FOR VARYING CITY SELECTION IN HOTELS, TRANSFERS AND SIGHTSEEING FIELDS BASED ON CITIES SELECTED IN QUOTE INFO
# $("#id_cities").change(function(){
#   var city_ids = $(this).val();
#   template = "<option value=''>---------</option>"
#   for (var i = 0; i < city_ids.length; i++) {
#     city = $("#id_cities option[value="+city_ids[i]+"]").text()
#     template += `<option value='${city_ids[i]}'>${city}</option>`
#     $("select[id*='city']").html(template)
#   }
# });
#
#
# // SCRIPT FOR VARYING HOTELS SELECTION BASED ON CITY SELECTED
# $(".hotel-selections select[id*='city']").change(function () {
#   id = this.id.replace('id_hotel-','').replace('-city','');
#   var url = $("#quoteForm").attr("data-hotels-url");
#   var city_id = $(this).val();
#   $.ajax({
#     url: url,
#     data: {
#       'city_id': city_id
#     },
#     success: function (data) {
#       var hotel_form_id = `id_hotel-${id}-hotel`
#       $(".hotel-selections select[id="+hotel_form_id+"]").html(data);
#     }
#   });
# });
#
#
# // SCRIPT FOR VARYING TRANSFERS SELECTION BASED ON CITY SELECTED
# $(".transfer-selections select[id*='city']").change(function () {
#   id = this.id.replace('id_transfer-','').replace('-city','');
#   var url = $("#quoteForm").attr("data-transfers-url");
#   var city_id = $(this).val();
#   $.ajax({
#     url: url,
#     data: {
#       'city_id': city_id
#     },
#     success: function (data) {
#       var transfer_form_id = `id_transfer-${id}-transfer`
#       $(".transfer-selections select[id="+transfer_form_id+"]").html(data);
#     }
#   });
# });
#
# // SCRIPT FOR VARYING SIGHTSEEINGS SELECTION BASED ON CITY SELECTED
# $(".sightseeing-selections select[id*='city']").change(function () {
#   id = this.id.replace('id_sightseeing-','').replace('-city','');
#   var url = $("#quoteForm").attr("data-sightseeings-url");
#   var city_id = $(this).val();
#   $.ajax({
#     url: url,
#     data: {
#       'city_id': city_id
#     },
#     success: function (data) {
#       var sightseeing_form_id = `id_sightseeing-${id}-sightseeing`
#       $(".sightseeing-selections select[id="+sightseeing_form_id+"]").html(data);
#     }
#   });
# });
#


##########################################################################
#   SalesApp
##########################################################################

# class CustomItineraryView(FormView):
#     template_name = 'SalesApp/custom_itinerary_form.html'
#
#     def create_itinerary_lists(self,ordering_list=None):
#         initial_quote = self.quote
#         itinerary_objects_list = []
#         itinerary_choices_objects_list = []
#         cities = initial_quote.cities.all()
#         trip_duration = (initial_quote.end_date - initial_quote.start_date).days + 1
#         current_itinerary_set = initial_quote.quoteitineraryinfo_set.all().order_by('date')
#
#         if not current_itinerary_set:
#             date = initial_quote.start_date
#             for i in range(trip_duration):
#                 QuoteItineraryInfo.objects.create(quote=initial_quote,date=date)
#                 date = date + timedelta(days=1)
#                 itinerary_objects_list.append([])
#             itinerary_choices_objects_list = (list(initial_quote.quotetransferinfo_set.all())
#                                                 + list(initial_quote.quotesightseeinginfo_set.all())
#                                                 + list(Transfer.objects.filter(city__in=cities,price=0))
#                                                 + list(Sightseeing.objects.filter(city__in=cities,adult_price=0,child_price=0))
#                                                 + list(initial_quote.quoteothersinfo_set.filter(type__in=['TRANSFER','SIGHTSEEING'])))
#         else:
#             transfer_qs_remove_ids = []
#             sightseeing_qs_remove_ids = []
#             free_transfer_qs_remove_ids = []
#             free_sightseeing_qs_remove_ids = []
#             others_qs_remove_ids = []
#             if ordering_list is None:
#                 ordering_list = []
#                 for object in current_itinerary_set:
#                     ordering_list.append(object.ordering)
#
#             current_days = current_itinerary_set.count()
#             extra_days = trip_duration - current_days
#             previous_start_date = current_itinerary_set.first().date
#
#             if previous_start_date != initial_quote.start_date: # CHECKS IF THE START DATE HAS CHANGED
#                 for object in current_itinerary_set:
#                     QuoteItineraryInfo.objects.update(date=date)
#                     date = date + timedelta(days=1)
#
#             if extra_days > 0: # CHECKS IF THE TRIP DURATION HAS CHANGED
#                 date = initial_quote.start_date + timedelta(days=current_days)
#                 for i in range(extra_days):
#                     QuoteItineraryInfo.objects.create(quote=initial_quote,date=date)
#                     date = date + timedelta(days=1)
#             elif extra_days < 0:
#                 delete_qs = QuoteItineraryInfo.objects.filter(date__gt=initial_quote.end_date)
#                 n = delete_qs.delete()[0] # queryset delete will give the no. of entries deleted
#                 ordering_list = ordering_list[0:trip_duration]
#
#             for ordering in ordering_list:
#                 items = ordering.split(',')
#                 object_list = []
#                 for item in items:
#                     if item:
#                         [object_type,id] = item.split('-')
#                         if object_type == 'transfer':
#                             try: # THIS WILL CHECK IF THE QUOTE-ITINERARY OBJECT HAS BEEN DELETED, OTHERWISE ADD IT TO DISPLAY LIST
#                                 object_list.append(QuoteTransferInfo.objects.get(id=id))
#                                 transfer_qs_remove_ids.append(id)
#                             except:
#                                 pass
#                         elif object_type == 'sightseeing':
#                             try: # THIS WILL CHECK IF THE QUOTE-SIGHTSEEING OBJECT HAS BEEN DELETED, OTHERWISE ADD IT TO DISPLAY LIST
#                                 object_list.append(QuoteSightseeingInfo.objects.get(id=id))
#                                 sightseeing_qs_remove_ids.append(id)
#                             except:
#                                 pass
#                         elif object_type == 'others':
#                             try: # THIS WILL CHECK IF THE QUOTE-OTHERS OBJECT HAS BEEN DELETED, OTHERWISE ADD IT TO DISPLAY LIST
#                                 object_list.append(QuoteOthersInfo.objects.get(id=id))
#                                 others_qs_remove_ids.append(id)
#                             except:
#                                 pass
#                         elif object_type == 'free_transfer':
#                             tr = Transfer.objects.get(id=id)
#                             if tr.city in cities:
#                                 object_list.append(tr)
#                                 free_transfer_qs_remove_ids.append(id)
#                         elif object_type == 'free_sightseeing':
#                             st = Sightseeing.objects.get(id=id)
#                             if st.city in cities:
#                                 object_list.append(st)
#                                 free_sightseeing_qs_remove_ids.append(id)
#                 itinerary_objects_list.append(object_list)
#
#
#             transfer_choices_qs = QuoteTransferInfo.objects.filter(quote=initial_quote).exclude(id__in=transfer_qs_remove_ids)
#             sightseeing_choices_qs = QuoteSightseeingInfo.objects.filter(quote=initial_quote).exclude(id__in=sightseeing_qs_remove_ids)
#             free_transfer_choices_qs = Transfer.objects.filter(city__in=cities,price=0).exclude(id__in=free_transfer_qs_remove_ids)
#             free_sightseeing_choices_qs = Sightseeing.objects.filter(city__in=cities,adult_price=0,child_price=0).exclude(id__in=free_sightseeing_qs_remove_ids)
#             others_choices_qs = QuoteOthersInfo.objects.filter(quote=initial_quote).filter(type__in=['TRANSFER','SIGHTSEEING']).exclude(id__in=others_qs_remove_ids)
#             itinerary_choices_objects_list = list(transfer_choices_qs) + list(sightseeing_choices_qs) + list(free_transfer_choices_qs) + list(free_sightseeing_choices_qs) + list(others_choices_qs)
#         return itinerary_objects_list,itinerary_choices_objects_list
#
#     def setup(self, request, *args, **kwargs):
#         """Initialize attributes shared by all view methods."""
#         self.request = request
#         self.args = args
#         self.kwargs = kwargs
#         self.quote_id = self.request.GET.get('quote_id')
#         self.quote = Quote.objects.get(id=self.quote_id)
#
#     def get(self, request, *args, **kwargs):
#         """ Handles GET requests and instantiates blank versions of the formsets. """
#         form = []
#         initial = [{'quote':self.quote}]
#         itinerary_formset = QuoteItineraryInfoFormSet(queryset=QuoteItineraryInfo.objects.filter(quote=self.quote),prefix='itinerary')
#         itinerary_objects_list,itinerary_choices_objects_list = self.create_itinerary_lists()
#         return self.render_to_response(self.get_context_data(form=form, itinerary_formset=itinerary_formset,itinerary_objects_list=itinerary_objects_list,
#                                                                 itinerary_choices_objects_list=itinerary_choices_objects_list))
#
#     def post(self, request, *args, **kwargs):
#         """
#         Handles POST requests, instantiating a form instance and its formsets with the passed POST variables and then checking them for validity.
#         """
#         initial = [{'quote':self.quote}]
#         itinerary_formset = QuoteItineraryInfoFormSet(self.request.POST,prefix='itinerary',initial=initial)
#
#         # GET THE ITINERARY ORDERING TO CONVERT THEM IN OBJECTS LIST FOR VIEW, IF THERE IS ERROR IN SAVING.
#         ordering_list = []
#         for form in itinerary_formset:
#             ordering_list.append(form['ordering'].value())
#         if (itinerary_formset.is_valid()):
#             return self.form_valid(itinerary_formset)
#         else:
#             itinerary_objects_list,itinerary_choices_objects_list = self.create_itinerary_lists(ordering_list=ordering_list)
#             return self.form_invalid(itinerary_formset,itinerary_objects_list,itinerary_choices_objects_list)
#
#     def form_valid(self,itinerary_formset):
#         """ Called if all forms are valid. Saves all formsets, updates quote boolean flags and then redirects to a success page. """
#         itinerary_formset.save()
#         self.quote.quote_itinerary = True
#         if self.quote.inclusions_updated:
#             self.quote.itinerary_updated = True
#             self.quote.quote_valid = True
#         self.quote.save()
#         return HttpResponseRedirect(reverse('SalesApp:quote_detail', args=[self.quote.id]))
#
#     def form_invalid(self,itinerary_formset,itinerary_objects_list,itinerary_choices_objects_list):
#         """ Called if a form is invalid. Re-renders the context data with the data-filled forms and errors. """
#         form = []
#         return self.render_to_response(self.get_context_data(form=form, itinerary_formset=itinerary_formset,
#                                                                         itinerary_objects_list=itinerary_objects_list,
#                                                                         itinerary_choices_objects_list=itinerary_choices_objects_list))

# class CustomInclusionsView(FormView):
#     template_name = 'SalesApp/custom_inclusions_form.html'
#
#     def setup(self, request, *args, **kwargs):
#         """Initialize attributes shared by all view methods."""
#         self.request = request
#         self.args = args
#         self.kwargs = kwargs
#         self.quote_id = self.request.GET.get('quote_id')
#         self.quote = Quote.objects.get(id=self.quote_id)
#
#     def get(self, request, *args, **kwargs):
#         """
#         Handles GET requests and instantiates blank versions of the formsets.
#         """
#         form = []
#         initial = [{'quote':self.quote}]
#         flight_formset = QuoteFlightInfoFormSet(queryset=QuoteFlightInfo.objects.filter(quote__id=self.quote_id),initial=initial,prefix='flight')
#         transport_formset = QuoteTransportInfoFormSet(queryset=QuoteTransportInfo.objects.filter(quote__id=self.quote_id),initial=initial,prefix='transport')
#         hotel_formset = QuoteHotelInfoFormSet(queryset=QuoteHotelInfo.objects.filter(quote__id=self.quote_id),initial=initial,prefix='hotel')
#         transfer_formset = QuoteTransferInfoFormSet(queryset=QuoteTransferInfo.objects.filter(quote__id=self.quote_id),initial=initial,prefix='transfer')
#         sightseeing_formset = QuoteSightseeingInfoFormSet(queryset=QuoteSightseeingInfo.objects.filter(quote__id=self.quote_id),initial=initial,prefix='sightseeing')
#         visa_formset = QuoteVisaInfoFormSet(queryset=QuoteVisaInfo.objects.filter(quote__id=self.quote_id),initial=initial,prefix='visa')
#         insurance_formset = QuoteInsuranceInfoFormSet(queryset=QuoteInsuranceInfo.objects.filter(quote__id=self.quote_id),initial=initial,prefix='insurance')
#         others_formset = QuoteOthersInfoFormSet(queryset=QuoteOthersInfo.objects.filter(quote__id=self.quote_id),initial=initial,prefix='others')
#         return self.render_to_response(self.get_context_data(form=form, flight_formset=flight_formset,
#                                                                         transport_formset=transport_formset,
#                                                                         hotel_formset=hotel_formset,
#                                                                         transfer_formset=transfer_formset,
#                                                                         sightseeing_formset=sightseeing_formset,
#                                                                         visa_formset=visa_formset,
#                                                                         insurance_formset=insurance_formset,
#                                                                         others_formset=others_formset))
#
#     def post(self, request, *args, **kwargs):
#         """
#         Handles POST requests, instantiating a form instance and its formsets with the passed POST variables and then checking them for validity.
#         """
#         initial = [{'quote':self.quote}]
#         flight_formset = QuoteFlightInfoFormSet(request.POST,prefix='flight',initial=initial)
#         transport_formset = QuoteTransportInfoFormSet(request.POST,prefix='transport',initial=initial)
#         hotel_formset = QuoteHotelInfoFormSet(request.POST,prefix='hotel',initial=initial)
#         transfer_formset = QuoteTransferInfoFormSet(request.POST,prefix='transfer',initial=initial)
#         sightseeing_formset = QuoteSightseeingInfoFormSet(request.POST,prefix='sightseeing',initial=initial)
#         visa_formset = QuoteVisaInfoFormSet(request.POST,prefix='visa',initial=initial)
#         insurance_formset = QuoteInsuranceInfoFormSet(request.POST,prefix='insurance',initial=initial)
#         others_formset = QuoteOthersInfoFormSet(request.POST,prefix='others',initial=initial)
#
#         if (flight_formset.is_valid() and transport_formset.is_valid() and hotel_formset.is_valid() and
#             transfer_formset.is_valid() and sightseeing_formset.is_valid() and visa_formset.is_valid() and
#             insurance_formset.is_valid() and others_formset.is_valid()):
#
#             return self.form_valid(flight_formset,transport_formset,hotel_formset,transfer_formset,sightseeing_formset,visa_formset,insurance_formset,others_formset)
#         else:
#             return self.form_invalid(flight_formset,transport_formset,hotel_formset,transfer_formset,sightseeing_formset,visa_formset,insurance_formset,others_formset)
#
#     def form_valid(self,flight_formset,transport_formset,hotel_formset,transfer_formset,sightseeing_formset,visa_formset,insurance_formset,others_formset):
#         """
#         Called if all forms are valid. Saves all formsets, updates quote boolean flags and then redirects to a success page.
#         """
#         flight_formset.save()
#         transport_formset.save()
#         hotel_formset.save()
#         transfer_formset.save()
#         sightseeing_formset.save()
#         visa_formset.save()
#         insurance_formset.save()
#         others_formset.save()
#
#         self.quote.quote_inclusions = True
#         self.quote.inclusions_updated = True
#         self.quote.inclusions_format = 'CUSTOM'
#         self.quote.itinerary_updated = False
#         self.quote.quote_valid = False
#
#         # CALCULATING PRICE
#         pricing_qs_list = (list(self.quote.quoteflightinfo_set.all()) + list(self.quote.quotetransportinfo_set.all()) + list(self.quote.quotehotelinfo_set.all())
#                             + list(self.quote.quotetransferinfo_set.all()) + list(self.quote.quotesightseeinginfo_set.all()) + list(self.quote.quotevisainfo_set.all())
#                             + list(self.quote.quoteinsuranceinfo_set.all()) + list(self.quote.quoteothersinfo_set.all()) )
#         price = 0
#         for object in pricing_qs_list:
#             if object.price:
#                 price += object.price
#         self.quote.price = price + self.quote.mark_up if self.quote.mark_up else price
#         self.quote.price = price - self.quote.discount if self.quote.discount else price
#         self.quote.save()
#         return HttpResponseRedirect(reverse('SalesApp:quote_detail', args=[self.quote.id]))
#
#     def form_invalid(self,flight_formset,transport_formset,hotel_formset,transfer_formset,sightseeing_formset,visa_formset,insurance_formset,others_formset):
#         """
#         Called if a form is invalid. Re-renders the context data with the data-filled forms and errors.
#         """
#         form = []
#         return self.render_to_response(self.get_context_data(form=form, flight_formset=flight_formset,
#                                                                         transport_formset=transport_formset,
#                                                                         hotel_formset=hotel_formset,
#                                                                         transfer_formset=transfer_formset,
#                                                                         sightseeing_formset=sightseeing_formset,
#                                                                         visa_formset=visa_formset,
#                                                                         insurance_formset=insurance_formset,
#                                                                         others_formset=others_formset))

# def create_itinerary_lists(self,ordering_list=None):
#     initial_quote = self.quote
#     itinerary_objects_list = []
#     itinerary_choices_objects_list = []
#     cities = initial_quote.cities.all()
#     trip_duration = (initial_quote.end_date - initial_quote.start_date).days + 1
#     current_itinerary_set = initial_quote.quoteitineraryinfo_set.all().order_by('date')
#
#     if not current_itinerary_set:
#         date = initial_quote.start_date
#         for i in range(trip_duration):
#             QuoteItineraryInfo.objects.create(quote=initial_quote,date=date)
#             date = date + timedelta(days=1)
#             itinerary_objects_list.append([])
#         itinerary_choices_objects_list = (list(initial_quote.quotetransferinfo_set.all())
#                                             + list(initial_quote.quotesightseeinginfo_set.all())
#                                             + list(Transfer.objects.filter(city__in=cities,price=0))
#                                             + list(Sightseeing.objects.filter(city__in=cities,adult_price=0,child_price=0))
#                                             + list(initial_quote.quoteothersinfo_set.filter(type__in=['TRANSFER','SIGHTSEEING'])))
#     else:
#         transfer_qs_remove_ids = []
#         sightseeing_qs_remove_ids = []
#         free_transfer_qs_remove_ids = []
#         free_sightseeing_qs_remove_ids = []
#         others_qs_remove_ids = []
#         if ordering_list is None:
#             ordering_list = []
#             for object in current_itinerary_set:
#                 ordering_list.append(object.ordering)
#
#         current_days = current_itinerary_set.count()
#         extra_days = trip_duration - current_days
#         previous_start_date = current_itinerary_set.first().date
#
#         if previous_start_date != initial_quote.start_date: # CHECKS IF THE START DATE HAS CHANGED
#             for object in current_itinerary_set:
#                 QuoteItineraryInfo.objects.update(date=date)
#                 date = date + timedelta(days=1)
#
#         if extra_days > 0: # CHECKS IF THE TRIP DURATION HAS CHANGED
#             date = initial_quote.start_date + timedelta(days=current_days)
#             for i in range(extra_days):
#                 QuoteItineraryInfo.objects.create(quote=initial_quote,date=date)
#                 date = date + timedelta(days=1)
#         elif extra_days < 0:
#             delete_qs = QuoteItineraryInfo.objects.filter(date__gt=initial_quote.end_date)
#             n = delete_qs.delete()[0] # queryset delete will give the no. of entries deleted
#             ordering_list = ordering_list[0:trip_duration]
#
#         for ordering in ordering_list:
#             items = ordering.split(',')
#             object_list = []
#             for item in items:
#                 if item:
#                     [object_type,id] = item.split('-')
#                     if object_type == 'transfer':
#                         try: # THIS WILL CHECK IF THE QUOTE-ITINERARY OBJECT HAS BEEN DELETED, OTHERWISE ADD IT TO DISPLAY LIST
#                             object_list.append(QuoteTransferInfo.objects.get(id=id))
#                             transfer_qs_remove_ids.append(id)
#                         except:
#                             pass
#                     elif object_type == 'sightseeing':
#                         try: # THIS WILL CHECK IF THE QUOTE-SIGHTSEEING OBJECT HAS BEEN DELETED, OTHERWISE ADD IT TO DISPLAY LIST
#                             object_list.append(QuoteSightseeingInfo.objects.get(id=id))
#                             sightseeing_qs_remove_ids.append(id)
#                         except:
#                             pass
#                     elif object_type == 'others':
#                         try: # THIS WILL CHECK IF THE QUOTE-OTHERS OBJECT HAS BEEN DELETED, OTHERWISE ADD IT TO DISPLAY LIST
#                             object_list.append(QuoteOthersInfo.objects.get(id=id))
#                             others_qs_remove_ids.append(id)
#                         except:
#                             pass
#                     elif object_type == 'free_transfer':
#                         tr = Transfer.objects.get(id=id)
#                         if tr.city in cities:
#                             object_list.append(tr)
#                             free_transfer_qs_remove_ids.append(id)
#                     elif object_type == 'free_sightseeing':
#                         st = Sightseeing.objects.get(id=id)
#                         if st.city in cities:
#                             object_list.append(st)
#                             free_sightseeing_qs_remove_ids.append(id)
#             itinerary_objects_list.append(object_list)
#
#
#         transfer_choices_qs = QuoteTransferInfo.objects.filter(quote=initial_quote).exclude(id__in=transfer_qs_remove_ids)
#         sightseeing_choices_qs = QuoteSightseeingInfo.objects.filter(quote=initial_quote).exclude(id__in=sightseeing_qs_remove_ids)
#         free_transfer_choices_qs = Transfer.objects.filter(city__in=cities,price=0).exclude(id__in=free_transfer_qs_remove_ids)
#         free_sightseeing_choices_qs = Sightseeing.objects.filter(city__in=cities,adult_price=0,child_price=0).exclude(id__in=free_sightseeing_qs_remove_ids)
#         others_choices_qs = QuoteOthersInfo.objects.filter(quote=initial_quote).filter(type__in=['TRANSFER','SIGHTSEEING']).exclude(id__in=others_qs_remove_ids)
#         itinerary_choices_objects_list = list(transfer_choices_qs) + list(sightseeing_choices_qs) + list(free_transfer_choices_qs) + list(free_sightseeing_choices_qs) + list(others_choices_qs)
#     return itinerary_objects_list,itinerary_choices_objects_list


# class QuoteFlightInfoForm(forms.ModelForm):
#     quote = forms.ModelChoiceField(queryset=Quote.objects.all(),disabled=True,required=False)
#     price = forms.FloatField(min_value=0)
#     class Meta:
#         model = QuoteFlightInfo
#         exclude = ()
#     def __init__(self, *args, **kwargs):
#         super(QuoteFlightInfoForm, self).__init__(*args, **kwargs)
#         self.empty_permitted = True
# QuoteFlightInfoFormSet = modelformset_factory(QuoteFlightInfo, form=QuoteFlightInfoForm, extra=0,can_delete=True)
#
# class QuoteTransportInfoForm(forms.ModelForm):
#     quote = forms.ModelChoiceField(queryset=Quote.objects.all(),disabled=True,required=False)
#     date = forms.DateField(widget=forms.DateInput(format='%d/%m/%y'),input_formats=('%d/%m/%y', ))
#     price = forms.FloatField(min_value=0)
#     class Meta:
#         model = QuoteTransportInfo
#         exclude = ()
#     def clean(self):
#         cleaned_data = super().clean()
#         date = cleaned_data.get("date")
#         quote = cleaned_data.get('quote')
#         if quote and date and (date < quote.start_date or date > quote.end_date):
#             self.add_error('date',"Date must be between trip start date and end date.")
#     def __init__(self, *args, **kwargs):
#         super(QuoteTransportInfoForm, self).__init__(*args, **kwargs)
#         self.empty_permitted = True
# QuoteTransportInfoFormSet = modelformset_factory(QuoteTransportInfo, form=QuoteTransportInfoForm, extra=1,can_delete=True)
#
# class QuoteHotelInfoForm(forms.ModelForm):
#     quote = forms.ModelChoiceField(queryset=Quote.objects.all(),disabled=True,required=False)
#     checkin_date = forms.DateField(widget=forms.DateInput(format='%d/%m/%y'),input_formats=('%d/%m/%y', ))
#     checkout_date = forms.DateField(widget=forms.DateInput(format='%d/%m/%y'),input_formats=('%d/%m/%y', ))
#     room_type = forms.CharField(initial='Standard Room',required=False)
#     no_of_rooms = forms.IntegerField(min_value=1,max_value=9,initial=1)
#     price = forms.FloatField(min_value=0)
#     class Meta:
#         model = QuoteHotelInfo
#         exclude = ()
#     def clean(self):
#         cleaned_data = super().clean()
#         city = cleaned_data.get("city")
#         hotel = cleaned_data.get("hotel")
#         checkin_date = cleaned_data.get('checkin_date')
#         checkout_date = cleaned_data.get('checkout_date')
#         quote = cleaned_data.get('quote')
#         if hotel and city and hotel.city != city:
#             self.add_error('hotel',"The hotel is not present in the selected city")
#         if  checkin_date and checkout_date and (checkout_date < checkin_date):
#             self.add_error('checkout_date',"Check out date cannot be before check in date.")
#         if checkin_date and quote and (checkin_date < quote.start_date or checkin_date > quote.end_date):
#             self.add_error('checkin_date',"Check in date must be between trip start date and end date.")
#         if checkout_date and quote and (checkout_date < quote.start_date or checkout_date > quote.end_date):
#             self.add_error('checkout_date',"Check out date must be between trip start date and end date.")
#     def __init__(self, *args, **kwargs):
#         super(QuoteHotelInfoForm, self).__init__(*args, **kwargs)
#         self.empty_permitted = True
#         if self.instance.pk:
#             self.fields['city'].queryset = self.instance.quote.cities.all().order_by('destination')
#             self.fields['hotel'].queryset = Hotel.objects.filter(city=self.instance.city).order_by('name')
#         # elif self.data:
#         #     city_ids = self.data.getlist('cities')
#         #     self.fields['city'].queryset = City.objects.filter(pk__in=city_ids).order_by('destination')
#         #     self.fields['hotel'].queryset = Hotel.objects.filter(city__id__in=city_ids).order_by('city')
#         else:
#             quote = kwargs.get('initial', None).get('quote',None)
#             self.fields['city'].queryset = quote.cities.all().order_by('destination')
#             self.fields['hotel'].queryset = Hotel.objects.filter(city__in=quote.cities.all())
# QuoteHotelInfoFormSet = modelformset_factory(QuoteHotelInfo, form=QuoteHotelInfoForm,extra=1,can_delete=True)
#
#
# class QuoteTransferInfoForm(forms.ModelForm):
#     quote = forms.ModelChoiceField(queryset=Quote.objects.all(),disabled=True,required=False)
#     transfer = forms.ModelChoiceField(queryset=Transfer.objects.filter(price__gt=0))
#     date = forms.DateField(widget=forms.DateInput(format='%d/%m/%y'),input_formats=('%d/%m/%y', ))
#     class Meta:
#         model = QuoteTransferInfo
#         exclude = ()
#     def clean(self):
#         cleaned_data = super().clean()
#         date = cleaned_data.get("date")
#         quote = cleaned_data.get('quote')
#         city = cleaned_data.get("city")
#         transfer = cleaned_data.get('transfer')
#         if quote and date and (date < quote.start_date or date > quote.end_date):
#             self.add_error('date',"Date must be between trip start date and end date.")
#         if transfer and city and transfer.city != city:
#             self.add_error('transfer',"This transfer is not present in the selected city")
#     def __init__(self, *args, **kwargs):
#         super(QuoteTransferInfoForm, self).__init__(*args, **kwargs)
#         self.empty_permitted = True
#         if self.instance.pk:
#             self.fields['city'].queryset = self.instance.quote.cities.all().order_by('destination')
#             self.fields['transfer'].queryset = Transfer.objects.filter(city=self.instance.city,price__gt=0)
#         else:
#             quote = kwargs.get('initial', None).get('quote',None)
#             self.fields['city'].queryset = quote.cities.all().order_by('destination')
#             self.fields['transfer'].queryset = Transfer.objects.filter(city__in=quote.cities.all(),price__gt=0)
# QuoteTransferInfoFormSet = modelformset_factory(QuoteTransferInfo, form=QuoteTransferInfoForm,extra=1,can_delete=True)
#
#
# class QuoteSightseeingInfoForm(forms.ModelForm):
#     quote = forms.ModelChoiceField(queryset=Quote.objects.all(),disabled=True,required=False)
#     sightseeing = forms.ModelChoiceField(queryset=Sightseeing.objects.filter(adult_price__gt=0,child_price__gt=0))
#     date = forms.DateField(widget=forms.DateInput(format='%d/%m/%y'),input_formats=('%d/%m/%y', ))
#     class Meta:
#         model = QuoteSightseeingInfo
#         exclude = ()
#     def clean(self):
#         cleaned_data = super().clean()
#         date = cleaned_data.get("date")
#         quote = cleaned_data.get('quote')
#         city = cleaned_data.get("city")
#         sightseeing = cleaned_data.get('sightseeing')
#         if quote and date and (date < quote.start_date or date > quote.end_date):
#             self.add_error('date',"Date must be between trip start date and end date.")
#         if sightseeing and city and sightseeing.city != city:
#             self.add_error('sightseeing',"This sightseeing tour is not present in the selected city")
#     def __init__(self, *args, **kwargs):
#         super(QuoteSightseeingInfoForm, self).__init__(*args, **kwargs)
#         self.empty_permitted = True
#         if self.instance.pk:
#             self.fields['city'].queryset = self.instance.quote.cities.all().order_by('destination')
#             self.fields['sightseeing'].queryset = Sightseeing.objects.filter(city=self.instance.city,adult_price__gt=0,child_price__gt=0).order_by('name')
#         else:
#             quote = kwargs.get('initial', None).get('quote',None)
#             self.fields['city'].queryset = quote.cities.all().order_by('destination')
#             self.fields['sightseeing'].queryset = Sightseeing.objects.filter(city__in=quote.cities.all(),adult_price__gt=0,child_price__gt=0).order_by('name')
# QuoteSightseeingInfoFormSet = modelformset_factory(QuoteSightseeingInfo, form=QuoteSightseeingInfoForm,extra=1,can_delete=True)
#
#
# class QuoteVisaInfoForm(forms.ModelForm):
#     quote = forms.ModelChoiceField(queryset=Quote.objects.all(),disabled=True,required=False)
#     class Meta:
#         model = QuoteSightseeingInfo
#         exclude = ()
#     def __init__(self, *args, **kwargs):
#         super(QuoteVisaInfoForm, self).__init__(*args, **kwargs)
#         self.empty_permitted = True
# QuoteVisaInfoFormSet = modelformset_factory(QuoteVisaInfo, form=QuoteVisaInfoForm,extra=1,can_delete=True)
#
# class QuoteInsuranceInfoForm(forms.ModelForm):
#     quote = forms.ModelChoiceField(queryset=Quote.objects.all(),disabled=True,required=False)
#     class Meta:
#         model = QuoteInsuranceInfo
#         exclude = ()
#     def __init__(self, *args, **kwargs):
#         super(QuoteInsuranceInfoForm, self).__init__(*args, **kwargs)
#         self.empty_permitted = True
# QuoteInsuranceInfoFormSet = modelformset_factory(QuoteInsuranceInfo, form=QuoteInsuranceInfoForm,extra=1,can_delete=True)
#
# class QuoteOthersInfoForm(forms.ModelForm):
#     quote = forms.ModelChoiceField(queryset=Quote.objects.all(),disabled=True,required=False)
#     date = forms.DateField(widget=forms.DateInput(format='%d/%m/%y'),input_formats=('%d/%m/%y', ),required=False)
#     price = forms.FloatField(min_value=0,required=False)
#     class Meta:
#         model = QuoteOthersInfo
#         exclude = ()
#     def clean(self):
#         cleaned_data = super().clean()
#         date = cleaned_data.get("date")
#         quote = cleaned_data.get('quote')
#         city = cleaned_data.get("city")
#         type = cleaned_data.get("type")
#         description = cleaned_data.get("description")
#         if date and (date < quote.start_date or date > quote.end_date):
#             self.add_error('date',"Date must be between trip start date and end date.")
#         if (type == 'TRANSFER' or type == 'SIGHTSEEING'):
#             if not city:
#                 self.add_error('city',"City must be specified for transfers or sightseeing.")
#             if not description:
#                 self.add_error('description',"Description must be specified for transfers or sightseeing.")
#             if not date:
#                 self.add_error('date',"Date must be specified for transfers or sightseeing.")
#     def __init__(self, *args, **kwargs):
#         super(QuoteOthersInfoForm, self).__init__(*args, **kwargs)
#         self.empty_permitted = True
#         if self.instance.pk:
#             self.fields['city'].queryset = self.instance.quote.cities.all().order_by('destination')
#         else:
#             quote = kwargs.get('initial', None).get('quote',None)
#             self.fields['city'].queryset = quote.cities.all().order_by('destination')
# QuoteOthersInfoFormSet = modelformset_factory(QuoteOthersInfo, form=QuoteOthersInfoForm, extra=1,can_delete=True)
#
# class QuoteItineraryInfoForm(forms.ModelForm):
#     quote = forms.ModelChoiceField(queryset=Quote.objects.all(),disabled=True,required=False)
#     class Meta:
#         model = QuoteItineraryInfo
#         exclude = ('description',)
#     def __init__(self, *args, **kwargs):
#         super(QuoteItineraryInfoForm, self).__init__(*args, **kwargs)
#         self.empty_permitted = True
# QuoteItineraryInfoFormSet = modelformset_factory(QuoteItineraryInfo, form=QuoteItineraryInfoForm,extra=0)


# class QuoteFlightInfo(models.Model):
#     quote = models.ForeignKey(Quote,on_delete=models.CASCADE,blank=True,null=True)
#     airline = models.CharField(max_length=255,blank=True)
#     details = models.TextField(max_length=1000)
#     remarks = models.CharField(max_length=255,blank=True)
#     price = models.FloatField(default=0)
#
# class QuoteTransportInfo(models.Model):
#     quote = models.ForeignKey(Quote,on_delete=models.CASCADE,blank=True,null=True)
#     type = models.CharField(max_length=100,choices=[('TRAIN','Train'),('BUS','Bus'),('FERRY','Ferry'),('TAXI','Taxi'),('CAR','Self Drive Car Rental')] )
#     date = models.DateField()
#     details = models.CharField(max_length=255)
#     price = models.FloatField(default=0)
#
# class QuoteHotelInfo(models.Model):
#     quote = models.ForeignKey(Quote,on_delete=models.CASCADE,blank=True,null=True)
#     city = models.ForeignKey(City,on_delete=models.PROTECT)
#     hotel = models.ForeignKey(Hotel,on_delete=models.PROTECT)
#     checkin_date = models.DateField()
#     checkout_date = models.DateField()
#     room_type = models.CharField(max_length=100,blank=True)
#     no_of_rooms = models.PositiveSmallIntegerField()
#     price = models.FloatField(default=0)
#
# class QuoteTransferInfo(models.Model):
#     quote = models.ForeignKey(Quote,on_delete=models.CASCADE,blank=True,null=True)
#     city = models.ForeignKey(City,on_delete=models.PROTECT)
#     transfer = models.ForeignKey(Transfer,on_delete=models.PROTECT)
#     date = models.DateField()
#     quantity = models.PositiveSmallIntegerField()
#
#     @property
#     def price(self):
#         return (self.quantity * self.transfer.price)
#
# class QuoteSightseeingInfo(models.Model):
#     quote = models.ForeignKey(Quote,on_delete=models.CASCADE,blank=True,null=True)
#     city = models.ForeignKey(City,on_delete=models.PROTECT)
#     sightseeing = models.ForeignKey(Sightseeing,on_delete=models.PROTECT)
#     date = models.DateField()
#
#     @property
#     def price(self):
#         return self.sightseeing.get_pricing(self.quote.adults,self.quote.children_age)
#
# class QuoteVisaInfo(models.Model):
#     quote = models.ForeignKey(Quote,on_delete=models.CASCADE,blank=True,null=True)
#     visa = models.ForeignKey(Visa,on_delete=models.PROTECT)
#
#     @property
#     def price(self):
#         return self.visa.get_pricing(self.quote.adults,self.quote.children_age)
#
# class QuoteInsuranceInfo(models.Model):
#     quote = models.ForeignKey(Quote,on_delete=models.CASCADE,blank=True,null=True)
#     insurance = models.ForeignKey(Insurance,on_delete=models.PROTECT,blank=True,null=True)
#
#     @property
#     def price(self):
#         children = self.quote.children if self.quote.children else 0
#         return self.insurance.price * (self.quote.adults + children)
#
# class QuoteOthersInfo(models.Model):
#     quote = models.ForeignKey(Quote,on_delete=models.CASCADE,blank=True,null=True)
#     name = models.CharField(max_length=255)
#     description = models.TextField(max_length=1000,blank=True)
#     date = models.DateField(blank=True,null=True)
#     price = models.FloatField(default=0)
#     type = models.CharField(max_length=100,choices=[('TRANSFER','Transfer'),('SIGHTSEEING','Sightseeing'),('OTHER','Other')],default='OTHER')
#     city = models.ForeignKey(City,on_delete=models.PROTECT, blank=True,null=True)
#
#     def __str__(self):
#         if self.city:
#             return '{} | {}'.format(self.name, self.city)
#         else:
#             return self.name
#
# class QuoteItineraryInfo(models.Model):
#     quote = models.ForeignKey(Quote,on_delete=models.CASCADE,blank=True,null=True)
#     date = models.DateField(blank=True,null=True)
#     ordering = models.CharField(max_length=255,blank=True)
#     description = models.TextField(blank=True)
