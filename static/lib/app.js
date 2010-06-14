/* app.js */
// override search links to use ajax_search as soon as possible
/* disabled until ajax_search fixed for logged-in people - JS error
$('a[href^="/search"]').each(function() {
	var href = $(this).attr('href');
	$(this).attr('href', href.replace("/search", "/pages/ajax_search"));
});*/
function parseQueryString(q) {
	var params = {};
	if(q.charAt(0)==="?") {
		q=q.substring(1);
	}
	q=q.replace(/\+/g," ");
	var pairs = q.split("&");
	var pair, key, value;
	for(var i=0; i<pairs.length; i++) {
		pair = decodeURIComponent(pairs[i]).split("=");
		key = pair[0];
		value = pair[1];
		if(value!=="") {
			if(!params[key]) {
				params[key] = [];
			}
			params[key].push(value);
		}
	}
	return params;
}
function redraw() { // IE6/7 position:relative elements not moving fix
	if($.browser.msie) {
		$('#columnPicker').css('display','none');
		$('#columnPicker').css('display','block');
	}
}
function addAdvSearchLine() {
	var container = '#advancedSearchContainer';
	
	var i = DependentInputs.createRow(container);
	var $row = DependentInputs.rows[i];
	
	var filterOnChange = function(elem,selectedIndex) {
		selectedIndex = selectedIndex || $row.field.get(0).selectedIndex;
		/* restore these lines when we can support "Any Field"
		if(selectedIndex===0) { // "Any Field"
			oTable.fnFilter(this.value);
		} else {
			// filter on columns assuming the select input doesn't include the AVID field
			oTable.fnFilter(this.value,selectedIndex);
		}*/
		
		/* we're going to look through the list of active filters and make sure there aren't any that shouldn't be there, which there will be if we've just changed a field */
		if(oTable) {
			var activeSearchLines = [];
			$('.advSearchLineField').each(function(i) {
				activeSearchLines.push($(this).attr('selectedIndex'));
			});
			var cols = oTable.fnSettings().aoPreSearchCols;
			$.each(cols, function(i) {
				if(this.sSearch) {
					if($.inArray(i,activeSearchLines)===-1) {
						this.sSearch="";
					}
				}
			});

			var val = elem ? elem.value : "";
			oTable.fnFilter(elem ? elem.value : "",selectedIndex);
			oTable.fixedHeader.fnUpdate(true);
		}
	};
	var filterByInput = function(event) {
		var target = event.target;
		if(!$(target).is("input")) {
			target = $(target).parent().find('input:text').get(0);
		}
		filterOnChange(target);
	};
	$row.change(function(event) {
		filterByInput(event);
	});
	$row.keyup(function(event) {
		filterByInput(event);
	});
	// reveal if not shown
	var $container = $(container);
	if($container.css('display')==="none") {
		$container.slideDown(250);
		/* have to put this here until FixedHeader can cope with the page changing length after it's been initialised - it's after a timeout because the revealAdvancedSearch function takes that long to complete */
		window.setTimeout(function() {
			if(oTable && oTable.fixedHeader) {
				oTable.fixedHeader.fnUpdate(true);
			}
		}, 300);
	}
	redraw();
	return $row;
}
function overflowTable(container,overflowTarget) {
	/* copy the entire table,
	   calculate the breaking point,
	   remove everything before the breaking point in the overflow column,
	   remove everything after the breaking point in the original column
	*/
	try {
	var $container = $(container), $overflowTarget = $(overflowTarget);
	if(!$container.length || !$overflowTarget.length) {
		return;
	}
	var breakingPoint = Math.floor($(container).find('tr').length / 2);
	var $point = $(overflowTarget).append($(container).html()).find('tr').eq(breakingPoint);
	$point.prevAll().remove();
	$point.closest('table').prevAll().remove();
	$point = $(container).find('tr').eq(breakingPoint-1);
	$point.nextAll().remove();
	$point.closest('table').nextAll().remove();
	} catch(ex) {
		console.log(ex);
	}
}
function makeCaptcha() {
	if($('#recaptcha').length) {
		Recaptcha.create("6Ld8HAgAAAAAAEIb34cZepZmJ0RlfeP6CmtoMO29", $('#recaptcha').get(0), {
			theme: 'red',
			callback: Recaptcha.focus_response_field
		});
	}
}
function makeModalAndSetValidator(idSelector) {
	var $origForm = $('#recordForm'); // shouldn't be a problem until you want to use more than one form on a page
	$('body').prepend('<div id="modal"><div class="overlay-decorator"></div><div class="overlay-wrap"><div class="overlay"><div class="dialog-decorator"></div><div class="dialog-wrap"><div class="dialog" id="dialog"><div class="content"><form id="tempForm"></form></div></div></div></div></div></div>');
	var $moved = $(idSelector).appendTo($('#modal #tempForm'));
	$('#tempForm').validate();
	$('#submitButton').clone().attr('id','submitButtonClone').appendTo($(idSelector)).click(function(e) {
		e.preventDefault();
		if(!$('#tempForm').valid()) {
			return;
		}
		$moved.find('input').each(function() {
			$('<input type="hidden" name="'+$(this).attr('name')+'" value="'+$(this).val()+'" />').appendTo($origForm);
		});
		$origForm.get(0).submit();
	});
	$('<button>Return to form</button>').appendTo($(idSelector))
	.addClass($('#submitButton').get(0).className)
	.css({
		float: 'left'
	}).click(function(e) {
		e.preventDefault();
		$('html').removeClass('modal');
	});
	$('#submitButton').click(function(e) {
		e.preventDefault();
		/* add operational state validation before validating form */
		var trigger_countries = ['United States'];
		$origForm.validate({
			rules: {
				_ignore_operational_state: {
					required: {
						depends: function(element) {
							var $r = $.map(DependentInputs.rows, function($row) {
								if($row.field.val()==="Operational Country") {
									return $row;
								}
							})[0];
							return $.inArray($r.val.val(),trigger_countries) >= 0 ? true : false;
						}
					}
				}
			}
		});
		if(!$origForm.valid()) {
			return;
		}
		$('#modal .overlay-decorator, #modal .overlay-wrap').css('top',$(window).scrollTop());
		$('html').addClass('modal');
		makeCaptcha();
	});
}
$(document).ready(function() {
	// overwrite default fields with dynamically generated list
	DependentInputs.fields = [];
	$.each(recordFields, function(i,pair) {
		//DependentInputs.fields.push(pair[0].replace(/__/g,"_(").replace(/_(\w)_/g,"($1)").replace(/_$/g,")").replace(/_/g," "));
		DependentInputs.fields.push(pair[1]);
	});
	// set advanced search on a slider
	$('#search .advanced').click(function() {
		addAdvSearchLine();
		return false;
	});
	$('#tableinfo .filter a').click(function() {
		addAdvSearchLine();
		return false;
	});
	$('#advancedSearchContainer').bind("mouseup",function() { // most ridiculous hack yet - fixing IE6/7 position:relative redraw problem
		window.setTimeout(function() {
			redraw();
		},0);
	});
	// fill in search box and filters with current query
	var q = window.location.search;
	if(q) {
		var params = parseQueryString(q);
		if(params.branches) {
			$('#branches').attr('checked', true);
		}
		if(params.q) {
			$('#company_search_box').val(params.q.join(" "));
		}
		for(var i in params) {
			if(i.match(/adv_\d{1,2}_field/)) {
				var val = params[i.replace('_field', '_value')];
				if(val && val[0]) {
					addAdvSearchLine()
						.find('input')
						.val(val[0])
						.prev()
						.val(params[i].join(" "))
						.change();
				}
			}
		}
	}
	if($('.operational_country, .operational_state, .registered_country, .registered_state').length) {
		var replaceCode = function(elem,code) {
			if(code) {
				var stateMap;
				stateMap = ISO_3166[code.toLowerCase()] || ISO_3166["2:"+code];
				if(stateMap) {
					$(elem).text(stateMap.iso2name[$(elem).text()]);
				}
			}
		};
		$('.operational_state').each(function() {
			var code = $.trim($('.operational_country').text());
			replaceCode(this,code);
		});
		$('.registered_state').each(function() {
			var code = $.trim($('.registered_country').text());
			replaceCode(this,code);
		});
		$('.operational_country, .registered_country').each(function(i) {
			$(this).text(ISO_3166.countries.iso2name[$(this).text()]);
		});
	}
	if($('#recordForm').length!==0) {
		DependentInputs.addDependency(function($row,changed) {
			if(changed==="field" && $row.field.attr("for")==="country") {
				$row.valueMap = ISO_3166.countries.name2iso;
				return DependentInputs.values.countries;
			}
		});
		overflowTable('#fieldsColumn','#tableoverflow'); // add before DependentInputs kicks in, otherwise you lose references to correct inputs after overflow
		if($('table.fields label').length) {
			DependentInputs.addRows('table.fields',"label[class!=error]",":input","tr");
		}
		if($('div.right label[for=country]+input').length) {
			DependentInputs.addRow('div.right',"label[for=country]","label[for=country]+input");
		}
		makeModalAndSetValidator('#personal_info');
		if($('div.captcha_error, label.error').length) {
			$('#submitButton').click();
		}
		var $hiddenWhileRendering = $('table.fields, div.right, #tableoverflow');
		if($hiddenWhileRendering.length) {
			$hiddenWhileRendering.css("visibility","visible");
		}
	}
	if($('#backnav').length) {
		$('#backnav').click(function() {
			window.history.go(-1);
			return false;
		});
	}
	if($('#registerform').length) {
		/* JRL: in search of a way to remove the company field error when independent checkbox is toggled
		var onclick_old = $.validator.defaults.onclick;
		console.log(onclick_old);
		$.validator.defaults.onclick = function() {
			console.log('onclick');
			$('#company').focus().blur();
			onclick_old.apply(this,arguments);
		};*/
		$('#registerform').validate({
			rules: {
				company: {
					required: {
						depends: function(element) {
							return $("#independent:unchecked").length;
						}
					}
				}
			}
			//focusCleanup: true,
			//focusInvalid: false
		});
	}
	// now show hidden things
	$('.onlyjs').css('visibility','visible');
});
