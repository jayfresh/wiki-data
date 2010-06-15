/* to move tabs into a clickable tab interface */
$(document).ready(function() {
	var tabWidth, tabMargin, newWidth;
	var $companyDiv = $('#recordcontainer');
	if($companyDiv.length) {
		$('#recordcontainer .record').each(function() {
			var $elem = $(this);
			$elem.css({'float':'left'});
			$('.entitycontent', $elem).css({
				"position":"absolute",
				"left":"0"
			});
			if(!$elem.hasClass("selected")) {
				$('.entitycontent',$elem).hide();
			}
		});
		$('#recordcontainer .tab h3').css('position','relative'); // otherwise you can't see the h3's in Safari
		$('#recordcontainer .tab').click(function() {
			var i = $('#recordcontainer .tab').index(this);
			$('#recordcontainer .record.selected').removeClass('selected').find('.entitycontent').hide();
			var $entitycontent = $(this).parent().addClass('selected').end().next();
			if(i>0) {
				$entitycontent.css({
					"left": -($(this).width()*i + 5*(i-1))
				});
			}
			$entitycontent.show();
			var origHeight = $('#recordcontainer').height();
			var overlap = origHeight+$companyDiv.offset().top - ($entitycontent.height()+$entitycontent.offset().top);
			/* 24 is entitycontent padding; 10 is added spacing around alt-buttons */
			$('#recordcontainer').height(origHeight-overlap+24+$('.alt-buttons:eq(0)').height()+10);
			/* that calculation is not efficient, but more understandable than removing origHeight from equation */
		}).each(function(i) {
			if(i!==0) {
				$(this).css("margin-left","5px");
			}
		});
		$companyDiv.removeClass('hide').css("visibility", "visible");
		$('#recordcontainer .tab').eq(0).click();
		
		
		// fix up state codes
		var findStateMap = function(country) {
			if(country==='Australia') {
				return ISO_3166['2:AU'].iso2name;
			} else if(country==='Canada') {
				return ISO_3166['2:CA'].iso2name;
			} else if(country==='USA') {
				return ISO_3166.usa.iso2name;
			}
		};
		var $op_address_div = $('#op_address_div');
		var country = $op_address_div.find('.operational_country').text();
		var stateMap = findStateMap(country);
		var state;
		if(stateMap) {
			state = stateMap[$op_address_div.find('.operational_state').text()];
			if(state) {
				$op_address_div.find('.operational_state').text(state);
			}
		}
		var $reg_address_div = $('#reg_address_div');
		country = $reg_address_div.find('.registered_country').text();
		stateMap = findStateMap(country);
		if(stateMap) {
			state = stateMap[$reg_address_div.find('.registered_state').text()];
			if(state) {
				$reg_address_div.find('.registered_state').text(state);
			}
		}
		
		// fix entity type codes
		var entity_name_map = {
			"TP": "Ultimate Parent",
			"LE": "Subsidiary",
			"SLE": "Branch",
			"BRA": "Branch"
		};
		var entity_code = $('.entity_type').text();
		if(entity_code) {
			var entity = entity_name_map[entity_code];
			if(entity) {
				$('.entity_type').text(entity);
			}
		}
				
		var makeAddressText = function(selector) {
			var $elem = $(selector);
			return $.trim((//$companyDiv.find('.adr .street-address').text() + " " +
				$elem.find('.adr .locality').text() + " " +
				$elem.find('.adr .region').text() + " " +
				$elem.find('.adr .country-name').text() + " " +
				$elem.find('.adr .postal-code').text()).replace(/[\n|\r]/g,"").replace(/(\s)+/g," "));
		};
		window.gMaps.op_address = makeAddressText('#op_address_div');
		if($('#reg_address_div').length) {
			window.gMaps.reg_address = makeAddressText('#reg_address_div');
		}
	}
});