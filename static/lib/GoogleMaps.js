$(document).ready(function() {
	var gMapsHost = window.gMaps ? "http://www.google.com/jsapi?key="+window.gMaps.apiKey : "";
	if(gMapsHost) {
		function gLoad(mapSelector, address) {
			google.load("maps", "2", {
				"callback" : function() {
					try {
						var map;
						var op_company = window.gMaps.op_company;
						var company;
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
						map = new google.maps.Map2($(mapSelector).get(0));
						map.addControl(new google.maps.SmallMapControl());
						map.addControl(new google.maps.MapTypeControl());
						// Create new geocoding object
						var geocoder = new google.maps.ClientGeocoder();
						// Retrieve location information, pass it to addToMap()
						company = op_company + "<br/>"+ address;
						geocoder.getLocations(address, addToMap);
					} catch(ex) {
						$(mapSelector).html('<p>error loading map</p>');
					}
				}
			});
		}
		var toInitialize = {
			'operational_map' : {
				address: window.gMaps.op_address,
				initialized: false
			},
			'registered_map' : {
				address: window.gMaps.reg_address,
				initialized: false
			}
		};
		var initCount = 2;
		window.mapsInitialize = function() {
			$.each(toInitialize, function(id, value) {
				var selector = '#'+id;
				if(initCount && $(selector).is(":visible") && !value.initialized) {				
					value.initialized = true;
					initCount--;
					gLoad(selector, value.address);
				}
			});
			if(initCount) {
				window.setTimeout(window.mapsInitialize,1000);
			}
		};
		gMapsHost += "&callback=mapsInitialize";
		$.getScript(gMapsHost);
	}
});