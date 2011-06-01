/* records.js */
var oTable;
var defaultView = [
	"avid",
	"legal_name",
	"trading_status",
	"registered_country",
	"operational_street_1",
	"operational_city",
	"operational_state",
	"operational_country",
	"entity_type"
];
var entity_name_map = {
	"TP": "Ultimate Parent",
	"LE": "Subsidiary",
	"SLE": "Branch",
	"BRA": "Branch"
};
var aoColumnsRenderMap = {
	"registered_country": function(data) {
		return ISO_3166.countries.iso2name[data.aData[data.iDataColumn]] || "";
	},
	"operational_state": function(data) {
		var country = ISO_3166.countries.iso2name[data.aData[aoColumnsRenderMap.operational_country_index]]; // aoColumnsRenderMap.operational_country_index gets set in another function - this method allows us to cope with tables that are different column sizes
		var mapping;
		var state;
		switch(country) {
			case "Australia":
				mapping = ISO_3166["2:AU"];
				break;
			case "Canada":
				mapping = ISO_3166["2:CA"];
				break;
			case "United States":
				mapping = ISO_3166.usa;
				break;
			default:
				// nothing
				break;
		}
		/* this line shows operational_state if is there
		state = mapping ? mapping.iso2name[data.aData[data.iDataColumn]] : data.aData[data.iDataColumn];*/
		state = (mapping && mapping.iso2name[data.aData[data.iDataColumn]]) ? mapping.iso2name[data.aData[data.iDataColumn]] : "";
		return state;
	},
	"operational_country": function(data) {
		return ISO_3166.countries.iso2name[data.aData[data.iDataColumn]] || "";
	},
	"entity_type": function(data) {
		return entity_name_map[data.aData[data.iDataColumn]] || "";
	}
};
$(document).ready(function() {
	// set up records table
	var aoColumns = [],
		field,
		options,
		i,
		il;
	for(i=0, il=recordFields.length; i<il; i++) {
		field = recordFields[i][0];
		options = {};
		if($.inArray(field,defaultView)===-1) {
			options.bVisible = false;
		}
		if(field==="legal_name") {
			options.sType = "html";
		}
		if(field==="operational_country") {
			aoColumnsRenderMap.operational_country_index = i;
		}
		if(field in aoColumnsRenderMap) {
			options.fnRender = aoColumnsRenderMap[field];
		}
		aoColumns.push(options);
	}
	aoColumns.push(
		{ sClass: "center", bSortable: false }, // challenge
		{ sClass: "center", bSortable: false }  // request more information
	);
	var $table = $('#resultsTable');
	if($table.length!==0) {
		options = {
			bAutoWidth: false,
			bPaginate: false,
			bSortClasses: false,
			bInfo: false,
			aaSorting: [],
			aoColumns: aoColumns,
			sDom: 't'
		};
		
		var setUpTable = function() {
			var columns;
			function getTitles() {
				var titles = [];
				for(var i=0;i<columns.length;i++) {
					titles.push(columns[i].sTitle);
				}
				return titles;
			}
			function hideColumn(col) {
				if(columns[col].bVisible) {
					oTable.fnSetColumnVis(col, false);
				}
				//oTable.fixedHeader.fnUpdate();
			}
			function showColumn(col) {
				if(!columns[col].bVisible) {
					oTable.fnSetColumnVis(col, true);
				}
				//oTable.fixedHeader.fnUpdate();
			}
			function toggleColumn(col) {
				if(columns[col].bVisible) {
					oTable.fnSetColumnVis(col, false);
				} else {
					oTable.fnSetColumnVis(col, true);
				}
				if($.browser.msie && $.browser.version.indexOf('8')!==-1) { // IE8 fix to redraw arrows so their bodies realign with their tips
					$('a.pointed').css('display','none');
					$('a.pointed').css('display','block');
				}
				//oTable.fixedHeader.fnUpdate();
			}
			$('#resultsTable').css('visibility',"visible");
			//$.fn.dragColumns('#resultsTable'); // JRL: debug
			//oTable.fixedHeader = new $.fn.dataTableExt.FixedHeader(oTable);
			columns = oTable.fnSettings().aoColumns;
			/* there is no tfoot in the new design
			$('#resultsTable tfoot th').live("click",function() {
				var i = $('#resultsTable tfoot th').index(this);
				var head = $('#resultsTable thead th')[i];
				var title = head.innerHTML;
				var titles = getTitles();
				var pos = $.inArray(title, titles);
				hideColumn(pos);
				return false;
			});
			*/
			var $labels = $('#columnPicker span.controls label');
			var $controls = $('#columnPicker span.controls input');
			var updateControlList = function() {
				var titles = getTitles();
				$controls.each(function(i) {
					if(!columns[i].bVisible) {
						$(this).attr("checked", "");
					} else {
						$(this).attr("checked", "checked");
					}
				});
			};
			updateControlList();
			$controls.click(function() {
				var i = $controls.index(this);
				var label = $labels[i].innerHTML;
				var titles = getTitles();
				var pos = $.inArray(label, titles);
				toggleColumn(pos);
			});
			
			var getPagingLink = function(elem) {
				var label = $(elem).text();
				var direction = label==="next" ? 1 : -1;
				var diff = direction*$('#pageDistance').text();
				var q = window.location.search;
				var start = q.indexOf('index=');
				var s = "";
				if(start===-1) { // diff can only be positive as we're at the start
					if(direction===-1) {
						return q;
					}
					s = q+"&index="+diff;
				} else {
					var end = q.indexOf('&',start);
					if(end===-1) {
						end = q.length;
					}
					var index = q.substring(start+6,end);
					var newIndex = parseInt(index,10)+diff;
					s = q.substring(0,start+6)+newIndex;
				}
				return s;
			};
			$('a.pagebutton').click(function() {
				if(!$(this).hasClass('inactive')) {
					window.location = getPagingLink(this);	
				}
				return false;
			});
			$('a.pagebutton').hover(function() {
				if(!$(this).hasClass('inactive') && $(this).attr('href')==='#') {
					$(this).attr('href', getPagingLink(this));
				}
			});
		};
		
		if(window.asyncSearch) { // disabled this on Feb 1st 2010
			var q = window.location.search;
			options.sAjaxSource = "/search.json"+q;
			options.fnInitComplete = setUpTable;
			options.fnServerData = function(url, data, callback) {
				var mapToDataTables = function(json) {
					var mapped = {"aaData":[]};
					var tiddler, fields;
					var count = json.length;
					var row;
					for(var i=0; i<count; i++) {
						tiddler = json[i];
						fields = tiddler.fields;
						row = [];
						for(var j=0, jl=recordFields.length; j<jl; j++) {
							if(j===0) {
								row.push('<a href="/bags/avox/tiddlers/'+tiddler.title+'.html">'+tiddler.title+'</a>'); // AVID
							}
							field = recordFields[j][0];
							row.push(fields[field] || "");
						}
						row.push('<a href="/bags/avox/tiddlers/'+tiddler.title+'.challenge">go</a>');
						row.push('<a href="/bags/avox/tiddlers/'+tiddler.title+'.request">go</a>');
						mapped.aaData.push(row);
					}
					var str = 'There are '+count+' results';
					switch(count) {
						case 0:
							str = 'There are no results - try <span class="filter"><a href="#">adding a filter</a></span> to include other fields in your search or <a href="/pages/suggest_new">register an entity</a>';
							break;
						case 1:
							str = 'There is 1 result';
							// deliberate fall-through
						case 51:
							str = 'There are more than 50 results, only showing the first 50';
							// deliberate fall-through
						default:
							str += ' - <span class="filter"><a href="javascript:;">add a filter</a>?</span>';
							break;
					}
					$('#results_count').html(str);
					callback(mapped);
				};
				$.getJSON(url, data, mapToDataTables);
			};
		}
		oTable = $table.dataTable(options);
		if(!window.asyncSearch) {
			setUpTable();
		}
	}
});
