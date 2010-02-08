$(document).ready(function() {
	var gMapsHost = window.gMaps ? "http://www.google.com/jsapi?key="+window.gMaps.apiKey : "";
	if(gMapsHost) {
		function gLoad(mapSelector, address) {
			google.load("maps", "2", {
				"callback" : function() {
					var map;
					var op_company = window.gMaps.op_company;
					var addToMap = function(response) {
						// Retrieve the object
						var place = response.Placemark[0];
						// Retrieve the latitude and longitude
						var point = new google.maps.LatLng(place.Point.coordinates[1],
						                  place.Point.coordinates[0]);
						// Center the map on this point
						map.setCenter(point, 3);
						map.setZoom(14);
						// Create a marker
						var marker = new google.maps.Marker(point);
						// Add the marker to map
						map.addOverlay(marker);
						// Add address information to marker
						marker.openInfoWindowHtml(company);
					};
					// Create new map object
					map = new google.maps.Map2($(mapSelector));
					map.addControl(new google.maps.SmallMapControl());
					map.addControl(new google.maps.MapTypeControl());
					// Create new geocoding object
					var geocoder = new google.maps.ClientGeocoder();
					// Retrieve location information, pass it to addToMap()
					var company = op_company + "<br/>"+ address;
					geocoder.getLocations(address, addToMap);
				}
			});
		}
		window.mapsInitialize = function() {
			if($('#operational_map').is(":visible")) {
				gLoad('#operational_map',window.gMaps.op_address);
			} else if($('#registered_map').is(":visible")) {
				gLoad('#registered_map', window.gMaps.reg_address);
			} else {
				window.setTimeout(window.mapsInitialize,1000);
			}
		};
		gMapsHost += "&callback=mapsInitialize";
		$.getScript(gMapsHost);
	}
});