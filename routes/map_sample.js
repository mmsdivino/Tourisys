  function initMap() {
    var directionsDisplay = new google.maps.DirectionsRenderer;
    var directionsService = new google.maps.DirectionsService;
    var latLngWaypoints = getLatLng();
    var map = new google.maps.Map(document.getElementById('map'), {
      zoom: 14,
      center: {lat: -12.8996, lng: -38.4035924}
    });
    directionsDisplay.setMap(map);

    calculateAndDisplayRoute(directionsService, directionsDisplay, latLngWaypoints);
    document.getElementById('mode').addEventListener('change', function() {
      calculateAndDisplayRoute(directionsService, directionsDisplay);
    });
  }

  function calculateAndDisplayRoute(directionsService, directionsDisplay, latLngWaypoints) {
    var selectedMode = document.getElementById('mode').value;
    directionsService.route({
      origin: {lat: -12.9691679, lng: -38.5106662},
      destination: {lat: -12.9725135, lng: -38.5090783},
      waypoints: latLngWaypoints,
      // Note that Javascript allows us to access the constant
      // using square brackets and a string value as its
      // "property."
      travelMode: google.maps.TravelMode[selectedMode]
    }, function(response, status) {
      if (status == 'OK') {
        directionsDisplay.setDirections(response);
      } else {
        window.alert('Directions request failed due to ' + status);
      }
    });
  }

  function getLatLng() {
      var list = [];
      waypoints.forEach(function(element) {
          loc = {location: new google.maps.LatLng(element.lat, element.lng)}
          list.push(loc)
      });
      return list
  }