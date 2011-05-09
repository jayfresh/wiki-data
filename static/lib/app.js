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
// TO-DO: see where this is used on redesign
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
			//oTable.fixedHeader.fnUpdate(true);
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
		/*window.setTimeout(function() {
			if(oTable && oTable.fixedHeader) {
				oTable.fixedHeader.fnUpdate(true);
			}
		}, 300);*/
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
	
	// JRL: this is not so straightforward anymore, now there are multiple structures for the form pages
	
	//try { // JRL: why is there a try/catch block here?
		var $container = $(container),
			$overflowTarget = $(overflowTarget),
			breakingPoint,
			$point,
			mode = $(".challengeForm").length,
			rowSelector = mode ? "input[type=text]" : "div";
		if(!$container.length || !$overflowTarget.length) {
			return;
		}
		breakingPoint = Math.floor($container.find(rowSelector).length / 2);
		if(mode) {
			$point = $overflowTarget
				.prepend($container.html())
				.find(rowSelector).eq(breakingPoint);
			$point.closest('tr')
				.prevAll().remove();
			$point.closest('div')
				.prevAll().remove();
			$point = $container
				.find(rowSelector).eq(breakingPoint-1);
			$point.closest('tr')
				.next()
				.nextAll().remove();
			$point.closest('div')
				.nextAll().remove();
		} else {
			$overflowTarget
				.prepend($container.html())
				.find(rowSelector).eq(breakingPoint)
				.prevAll().remove();
			$container
				.find(rowSelector).eq(breakingPoint-1)
				.nextAll().remove();
		}
		
	/*} catch(ex) {
		console.log(ex);
	}*/
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
	$('body').prepend('<div id="modal" class="jbasewrap"><div class="overlay-decorator"></div><div class="overlay-wrap"><div class="overlay"><div class="dialog-decorator"></div><div class="dialog-wrap"><div class="dialog" id="dialog"><div class="content"><form id="tempForm"></form></div></div></div></div></div></div>');
	var $moved = $(idSelector).appendTo($('#modal #tempForm'));
	$('#tempForm').validate();
	$('#submitButton').clone().attr('id','submitButtonClone').addClass('right').appendTo($(idSelector)).click(function(e) {
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
	.addClass($('#submitButton').get(0).className+" left")
	.click(function(e) {
		e.preventDefault();
		$('html').removeClass('modal');
	});
	$('<br class="clearboth" />').appendTo($(idSelector));
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

$.fn.equalize = function() {
	var $collection = this,
		heights = [],
		maxHeight;
	$collection.each(function(i, elem) {
		heights.push($(elem).height());
	});
	maxHeight = Math.max.apply(Math, heights);
	$collection.height(maxHeight);
	return this;
};

$(document).ready(function() {
	// overwrite default fields with dynamically generated list
	DependentInputs.fields = [];
	$.each(recordFields, function(i,pair) {
		//DependentInputs.fields.push(pair[0].replace(/__/g,"_(").replace(/_(\w)_/g,"($1)").replace(/_$/g,")").replace(/_/g," "));
		DependentInputs.fields.push(pair[1]);
	});
	// set advanced search on a slider
	$('#searchBox button').click(function(e) {
		e.preventDefault();
		addAdvSearchLine();
		return false;
	});
	$('.tableinfo a.addFilter').click(function(e) {
		e.preventDefault();
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
			$('#branches').attr('checked', 'checked');
		} else {
			$('#branches').attr('checked', '');
		}
		if(params.q) {
			$('#query').val(params.q.join(" "));
		}
		if(params.type) {
			$('#type').val(params.type);
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
		if($('#entity_type').length) {
			var entityMap = {
				"Ultimate Parent": "TP",
				"Subsidiary": "LE",
				"Branch": "SLE"
			},
			values = [];
			for(var i in entityMap) {
				values.push(i);
			}
			DependentInputs.addDependency(function($row,changed) {
				if(changed==="field" && $row.field.attr("for")==="entity_type") {
					$row.valueMap = entityMap;
					return values;
				}
			});
		}
		if($('#'))
		overflowTable('#toOverflow','#tableoverflow'); // add before DependentInputs kicks in, otherwise you lose references to correct inputs after overflow
		if($('#recordForm label').length) {
			DependentInputs.addRows('#recordForm',"label[class!=error]",":input[type=text], select");
		}
		if($('div.right label[for=country]+input').length) { // 'Your Country'
			DependentInputs.addRow('div.right',"label[for=country]","label[for=country]+input");
		}
		makeModalAndSetValidator('#personal_info');
		if($('div.captcha_error, label.error').length) {
			$('#submitButton').click();
		}
		var $hiddenWhileRendering = $('#tableoverflow, #toOverflow');
		if($hiddenWhileRendering.length) {
			$hiddenWhileRendering.css("visibility","visible");
		}
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
	$('.equalise1').equalize();
	// now show hidden things
	// TO-DO: see whether the onlyjs things are even hidden
	$('.onlyjs').css('visibility','visible');
});
