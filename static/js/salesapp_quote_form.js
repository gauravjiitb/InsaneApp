// SCRIPT FOR RENDERING CHILDREN AGE FIELDS
$('input[name*=children_age]').after("<small class='form-text text-muted'>Enter age of all children separated by commas as show above.</small>");;
$('input[name*=children_age]').attr('placeholder','4,12,9')
// $("label[for*='children_age']").parent().hide();
// $("input#id_children").on('change',function(){
//   var n = $(this).val();
//
//   if (n == 0) {
//     template = "<label for='id_children_age'></label>";
//     $("label[for*='children_age']").parent().hide();
//   } else{
//     template = "<label for='id_children_age'>Children age</label>";
//     for(var i = 0; i < n; i++){
//       template += `<input type="number" name="children_age" placeholder="Children ${i+1} age" class="form-control" required="" id="id_children_${i}_age" >`;
//     }
//
//   }
//   $("label[for*='children_age']").parent().html(template);
//   $("label[for*='children_age']").parent().show();
// });


// SCRIPT FOR VARYING CITY SELECTION IN QUOTE INFO BASED ON DESTINATIONS SELECTED
$("#id_destinations").change(function () {
  var url = $("#quoteForm").attr("data-cities-url");  // get the url of the `quote_load_cities` view
  var destination_ids = $(this).val();  // get the selected country ID from the HTML input

  $.ajax({                       // initialize an AJAX request
    url: url,                    // set the url of the request (= localhost:8000/sales/ajax/quote/load-cities/)
    data: {
      'destinations': destination_ids       // add the destination id to the GET parameters
    },
    success: function (data) {   // `data` is the return of the `load_cities` view function
      $("#id_cities").html(data);  // replace the contents of the city input with the data that came from the server
    }
  });
});


// SCRIPT FOR VARYING CITY SELECTION IN HOTELS, TRANSFERS AND SIGHTSEEING FIELDS BASED ON CITIES SELECTED IN QUOTE INFO
$("#id_cities").change(function(){
  var city_ids = $(this).val();
  template = "<option value=''>---------</option>"
  for (var i = 0; i < city_ids.length; i++) {
    city = $("#id_cities option[value="+city_ids[i]+"]").text()
    template += `<option value='${city_ids[i]}'>${city}</option>`
    $("select[id*='city']").html(template)
  }
});


// SCRIPT FOR VARYING HOTELS SELECTION BASED ON CITY SELECTED
$(".hotel-selections select[id*='city']").change(function () {
  id = this.id.replace('id_hotel-','').replace('-city','');
  var url = $("#quoteForm").attr("data-hotels-url");
  var city_id = $(this).val();
  $.ajax({
    url: url,
    data: {
      'city_id': city_id
    },
    success: function (data) {
      var hotel_form_id = `id_hotel-${id}-hotel`
      $(".hotel-selections select[id="+hotel_form_id+"]").html(data);
    }
  });
});


// SCRIPT FOR VARYING TRANSFERS SELECTION BASED ON CITY SELECTED
$(".transfer-selections select[id*='city']").change(function () {
  id = this.id.replace('id_transfer-','').replace('-city','');
  var url = $("#quoteForm").attr("data-transfers-url");
  var city_id = $(this).val();
  $.ajax({
    url: url,
    data: {
      'city_id': city_id
    },
    success: function (data) {
      var transfer_form_id = `id_transfer-${id}-transfer`
      $(".transfer-selections select[id="+transfer_form_id+"]").html(data);
    }
  });
});

// SCRIPT FOR VARYING SIGHTSEEINGS SELECTION BASED ON CITY SELECTED
$(".sightseeing-selections select[id*='city']").change(function () {
  id = this.id.replace('id_sightseeing-','').replace('-city','');
  var url = $("#quoteForm").attr("data-sightseeings-url");
  var city_id = $(this).val();
  $.ajax({
    url: url,
    data: {
      'city_id': city_id
    },
    success: function (data) {
      var sightseeing_form_id = `id_sightseeing-${id}-sightseeing`
      $(".sightseeing-selections select[id="+sightseeing_form_id+"]").html(data);
    }
  });
});
