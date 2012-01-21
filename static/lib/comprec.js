$(document).ready(function() {
	var $companyDiv = $('.companyRecord').css('visibility','hidden'),
		findStateMap,
		country,
		stateMap,
		state,
		entityNameMap,
		entityCode,
		entity,
		makeAddressText,
		address;
		
	if($companyDiv.length) {
		$('#backToSearch').click(function(e) {
			e.preventDefault();
			window.history.go(-1);
			return false;
		});
		
		// fix up state codes
		findStateMap = function(country) {
			if(country==='Australia') {
				return ISO_3166['2:AU'].iso2name;
			} else if(country==='Canada') {
				return ISO_3166['2:CA'].iso2name;
			} else if(country==='USA') {
				return ISO_3166.usa.iso2name;
			}
		};
		country = $('.operational_country:eq(0)').text();
		stateMap = findStateMap(country);
		if(stateMap) {
			state = stateMap[$('.operational_state:eq(0)').text()];
			if(state) {
				$('.operational_state:eq(0)').text(state);
			}
		}
		/* not needed unless registered state information is shown
		country = $('.registered_country:eq(0)').text();
		stateMap = findStateMap(country);
		if(stateMap) {
			state = stateMap[$('.registered_state:eq(0)').text()];
			if(state) {
				$('.registered_state:eq(0)').text(state);
			}
		}
		*/
		// fix entity type codes
		entityNameMap = {
			"TP": "Ultimate Parent",
			"LE": "Subsidiary",
			"SLE": "Branch",
			"BRA": "Branch"
		};
		entityCode = $('.entity_type').text();
		entity = entityNameMap[entityCode];
		if(entity) {
			$('.entity_type').text(entity);
		}

		makeAddressText = function(selector) {
			var $container = $(selector);
			return $.trim((
				$container.find('.street-address').text() + ", " +
				$container.find('.locality').text() + ", " +
				$container.find('.region').text() + ", " +
				$container.find('.country-name').text() + ", " +
				$container.find('.postal-code').text()).replace(/[\n|\r]/g,"").replace(/(\s)+/g," ").replace(/(, ){2,4}/g, ", "));
		};
		address = makeAddressText('.adr');
		$('a.viewmap').attr('href', 'http://maps.google.com/maps?q='+encodeURIComponent(address));
		/* not needed if registered address is not being shown
		if($('.registered_address').length) {
			window.gMaps.reg_address = makeAddressText('#reg_address_div');
		}
		*/
		
		// make help text headers and content the same width
		$companyDiv.find('.help').each(function() {
			var $header = $(this).find('span.heading span.text').css('width','auto'),
				$helpText = $(this).find('span.helpText'),
				headerWidth = $header.width(),
				helpTextWidth = $helpText.width(),
				widthAdjustment = 8; // this is to offset difference in header and helptext relative positions
			if(headerWidth<helpTextWidth) {
				$header.width(helpTextWidth+widthAdjustment+'px');
			}
			if(helpTextWidth<headerWidth) {
				$helpText.width(headerWidth-widthAdjustment+'px');
			}
				
		});
		
		$companyDiv.css('visibility', 'visible');
	}
});