
$.getScript( "https://maps.googleapis.com/maps/api/js?key=" + google_api_key + "&libraries=places")
.done(function( script, textStatus ) {
    google.maps.event.addDomListener(window, "load", initAutocomplete())

})

var auto_fields = ['a', 'b']

function initAutocomplete() {

  for (i = 0; i < auto_fields.length; i++) {
    var field = auto_fields[i]
    window['autocomplete_'+field] = new google.maps.places.Autocomplete(
      document.getElementById('id-google-address-' + field),
    {
       fields: ["name"],
       types: ['address'],
       componentRestrictions: {'country': [base_country.toLowerCase()]},
    })
  }

  autocomplete_a.addListener('place_changed', function(){
          onPlaceChanged('a')
      });
  autocomplete_b.addListener('place_changed', function(){
          onPlaceChanged('b')
      });
}


function onPlaceChanged (addy){

    var auto = window['autocomplete_'+addy]
    var el_id = 'id-google-address-'+addy
    var lat_id = 'id-lat-' + addy
    var long_id = 'id-long-' + addy
    var address_id = 'id-address-' + addy

    // Use Google Javascript Geocoding API to fetch latitude/longitude for an address
    var geocoder = new google.maps.Geocoder()
    var address = document.getElementById(el_id).value
    geocoder.geocode( { 'address': address}, function(results, status) {
        if (status == google.maps.GeocoderStatus.OK) {
            var latitude = results[0].geometry.location.lat();
            var longitude = results[0].geometry.location.lng();
            var address = results[0].formatted_address;

            $('#' + lat_id).val(latitude)
            $('#' + long_id).val(longitude)
            $('#' + address_id).val(address)

            CalcRoute()
        }
        else {
        alert("Geocode was not successful for the following reason: " + status);
        }
    });
}


function validateForm() {
    var valid = true;
    $('.geo').each(function () {
        if ($(this).val() === '') {
            valid = false;
            return false;
        }
    });
    return valid
}


function CalcRoute(){
    // example: GET /map?lat_a=37.3709131&long_a=-121.8776796&lat_b=37.4093765&long_b=-121.896497 HTTP/1.1
    if ( validateForm() == true){

      var params = {
          lat_a: $('#id-lat-a').val(),
          long_a: $('#id-long-a').val(),
          lat_b: $('#id-lat-b').val(),
          long_b: $('#id-long-b').val(),
          address_a:$('#id-address-a').val(),
          address_b:$('#id-address-b').val(),
      };

      var esc = encodeURIComponent;
      var query = Object.keys(params)
          .map(k => esc(k) + '=' + esc(params[k]))
          .join('&');

      url = '/map?' + query
      window.location.assign(url)
    }

}