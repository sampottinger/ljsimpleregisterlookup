var LOOKUP = "/lookup.json?"

var host = window.location.host;
var BASE_URL;

deployed = host.indexOf("0.0.0.0") == -1;
deployed = deployed && host.indexOf("127.0.0.1") == -1;
deployed = deployed && host.indexOf("localhost") == -1;
deployed = deployed && host.indexOf("c9") == -1;
if (deployed) {
    BASE_URL = "https://ljsimpleregisterlookup.herokuapp.com/";
} else {
    BASE_URL = '';
}


var DEPLOY_URL = BASE_URL + LOOKUP;
var LOCAL_TEST_URL = LOOKUP;

var CURRENT_APP_URL = DEPLOY_URL;

var anOpen = [];


function attachListeners(oTable, descriptionIndex, tableID)
{
    $(window).resize(function() {
        oTable.fnAdjustColumnSizing();
    });
    $("#" + tableID + " td.control").die("click");
    $("#" + tableID + " td.control").live("click", function () {
        var nTr = this.parentNode;

        var i = $.inArray( nTr, anOpen );

        if ( i === -1 )
        {
            $("img", this).attr( "src", BASE_URL + "/static/images/details_close.png" );
            var nDetailsRow = oTable.fnOpen( nTr, fnFormatDetails(oTable, nTr, descriptionIndex), "details" );
            $("div.innerDetails", nDetailsRow).slideDown();
            anOpen.push( nTr );
        }
        else
        {
            $("img", this).attr( "src", BASE_URL + "/static/images/details_open.png" );
            $("div.innerDetails", $(nTr).next()[0]).slideUp( function () {
                oTable.fnClose( nTr );
                anOpen.splice( i, 1 );
            } );
        }
    });
}


/**
 * Updates the registers data table with the given registers data.
 *
 * Re-initalizes the registers data table with server-provided registers data,
 * hiding the loading indiciator and showing the table in the process.
 *
 * @param {array} data Registers 2D array provided by the server.
**/
var updateRegistersTable = function(data, tableContainer)
{
    var tableID = tableContainer + "-table";

    // Create bare table
    var resultHTML = "<table cellpadding=\"0\" cellspacing=\"0\" border=\"0\"" +
    "class=\"display registerTable\" id=\"" + tableID + "\"></table>";
    $("#" + tableContainer).html(resultHTML);

    var columnNames = data[0]; // Header

    var descriptionIndex = columnNames.indexOf("description");
    columnNames.splice(descriptionIndex, 1);

    var nameIndex = columnNames.indexOf("name");

    // Generate columns
    var columns = columnNames.map(function(x) {
        return { "sTitle": x, "sClass": "left", "sWidth": "90px"};
    });

    columns[nameIndex].sWidth = "40px";

    // Add description column controls
    columns.push(
        {
            "sTitle": "details",
            "mDataProp": null,
            "sClass": "control center",
            "mRender": function(x) {
                var retCode = "<img src=\"";
                retCode += BASE_URL;
                retCode += "/static/images/details_open.png\">";
                return retCode;
            },
        }
    );

    // Remove header
    var headerlessData = data.slice(1);

    // Initialize data table
    var oTable = $("#" + tableContainer + "-table").dataTable( {
        "aaData": headerlessData,
        "aoColumns": columns,
        "aaSorting": [[ 1, "asc" ]],
        "bJQueryUI": true,
        "sPaginationType": "full_numbers",
        "bAutoWidth": false
    } );

    // http://datatables.net/forums/discussion/3835/width-columns-problem-in-chrome-safari/p1
    setTimeout( function () {
        oTable.fnAdjustColumnSizing();
    }, 10 );

    // Attach details link listeners
    attachListeners(oTable, descriptionIndex, tableID);

    // Show table
    $("#" + tableContainer).show();

}

function fnFormatDetails( oTable, nTr, descriptionIndex)
{
  var aData = oTable.fnGetData( nTr );
  var sOut =
    "<div class=\"innerDetails\">"+
        aData[descriptionIndex] +
    "</div>";
  return sOut;
}


function RegistersTableRequester()
{
    var device = null;
    var tags = null;
    var notTags = null;
    var regNames = null;
    var regAddrs = null;
    var expand = null;
    var includeCSS = true;
    var fields = null;

    this.setDevice = function(newVal)
    {
        device = newVal;
    }

    this.setTags = function(newVal)
    {
        if(newVal instanceof Array)
            newVal = newVal.join(",");
        tags = newVal;
    }

    this.setNotTags = function(newVal)
    {
        notTags = newVal;
    }

    this.setRegNames = function(newVal)
    {
        if(newVal instanceof Array)
            newVal = newVal.join(",");
        regNames = newVal;
    }

    this.setRegAddrs = function(newVal)
    {
        if(newVal instanceof Array)
            newVal = newVal.join(",");
        regAddrs = newVal;
    }

    this.setExpand = function(newVal)
    {
        expand = newVal;
    }

    this.setFields = function(newVal)
    {
        fields = newVal;
    }

    this.loadTable = function(tableContainer, callback)
    {
        var data = {};

        if(device != null)
            data["device_name"] = device;
        if(tags != null)
            data["tags"] = tags;
        if(notTags != null)
            data["not-tags"] = notTags;
        if(regNames != null)
            data["add-reg-names"] = regNames;
        if(regAddrs != null)
            data["add-regs"] = regAddrs;
        if(expand != null)
            data["expand-addresses"] = expand;
        if(fields != null)
            data["fields"] = fields;

        $.getJSON(
            CURRENT_APP_URL,
            data,
            function(data) {
                updateRegistersTable(data, tableContainer); 
                callback();
            }
        );
    }

}
