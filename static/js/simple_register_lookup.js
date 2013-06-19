/**
 * Javascript client-side controller for Simple Register Lookup.
 *
 * Client-side controller for the Simple Register Lookup, a web-based modbus
 * map lookup utility.
 *
 * @author Sam Pottinger
 * @license GNU GPL v2
**/
var LOOKUP = '/lookup.json?'

var DEPLOY_URL = 'http://ljsimpleregisterlookup.herokuapp.com' + LOOKUP;
var LOCAL_TEST_URL = LOOKUP;

var CURRENT_APP_URL = LOCAL_TEST_URL;

var anOpen = [];


// Thanks http://www.tutorialspoint.com/javascript/array_map.htm
if (!Array.prototype.map)
{
  Array.prototype.map = function(fun /*, thisp*/)
  {
    var len = this.length;
    if (typeof fun != "function")
      throw new TypeError();

    var res = new Array(len);
    var thisp = arguments[1];
    for (var i = 0; i < len; i++)
    {
      if (i in this)
        res[i] = fun.call(thisp, this[i], i, this);
    }

    return res;
  };
}


/**
 * Updates the registers data table with the given registers data.
 *
 * Re-initalizes the registers data table with server-provided registers data,
 * hiding the loading indiciator and showing the table in the process.
 *
 * @param {array} data Registers 2D array provided by the server.
**/
var updateRegistersTable = function(data)
{
    // Create bare table
    $('#register-table-container').html(
        '<table cellpadding="0" cellspacing="0" border="0" class="display" id="register-table"></table>'
    );

    var columnNames = data[0]; // Header

    var descriptionIndex = columnNames.indexOf("description");
    columnNames.splice(descriptionIndex, 1);

    // Generate columns
    var columns = columnNames.map(function(x) {
        return { "sTitle": x, "sClass": "left"};
    });

    // Add description column controls
    columns.push(
        {
            "sTitle": "details",
            "mDataProp": null,
            "sClass": "control center",
            "mRender": function(x) {
                return "<img src='/static/images/details_open.png'>";
            }
        }
    );

    // Remove header
    var headerlessData = data.slice(1);

    // Initialize data table
    var oTable = $('#register-table').dataTable( {
        "aaData": headerlessData,
        "aoColumns": columns,
        "aaSorting": [[ 1, "asc" ]],
        "bJQueryUI": true,
        "sPaginationType": "full_numbers",
        "sScrollX": "100%",
    } );

    // http://datatables.net/forums/discussion/3835/width-columns-problem-in-chrome-safari/p1
    setTimeout( function () {
        oTable.fnAdjustColumnSizing();
    }, 10 );

    // Attach details link listeners
    $("#register-table td.control").live("click", function () {
        var nTr = this.parentNode;
        var i = $.inArray( nTr, anOpen );

        if ( i === -1 )
        {
            $("img", this).attr( "src", "/static/images/details_close.png" );
            var nDetailsRow = oTable.fnOpen( nTr, fnFormatDetails(oTable, nTr, descriptionIndex), 'details' );
            $('div.innerDetails', nDetailsRow).slideDown();
            anOpen.push( nTr );
        }
        else
        {
            $("img", this).attr( "src", "/static/images/details_open.png" );
            $('div.innerDetails', $(nTr).next()[0]).slideUp( function () {
                oTable.fnClose( nTr );
                anOpen.splice( i, 1 );
            } );
        }
    });

    // Show table
    $('#register-table-container').show();
    $('#loading-image').hide();
}

function fnFormatDetails( oTable, nTr, descriptionIndex)
{
  var aData = oTable.fnGetData( nTr );
  var sOut =
    '<div class="innerDetails">'+
        aData[descriptionIndex] +
    '</div>';
  return sOut;
}


/**
 * Makes a async request for register data for the user-selected device.
 *
 * Starts an AJAX request for register data for the device selected in the
 * device-dropdown menu. Hides the data table and shows the loading / busy
 * indicator in the process.
**/
var requestRegistersTable = function()
{
    // Show loading indicator
    $('#error-message').hide();
    $('#register-table-container').hide();
    $('#loading-image').show();

    // Execute AJAX request
    // TODO: jQuery does not have an onError event for getJSON. Need workaround.
    $.getJSON(
        CURRENT_APP_URL
            + 'device_name=' + $("#device-dropdown").val()
            + '&tags=' + $("#tag-dropdown").val()
            + '&not-tags=' + $("#not-tag-dropdown").val()
            + '&add-reg-names=' + $("#add-reg-name-dropdown").val()
            + '&expand-addresses=' + $("#expand-checkbox").is(':checked'),
        updateRegistersTable
    );
}


var handleError = function(err)
{
    $('#loading-image').hide();

    // Probably don't want to expose anything, I'm not sure
    // what errors could be caught here.
    // $('#error-message').text("Error: " + err.message);
    $('#error-message').text("An error has occurred.");
    $('#error-message').show();
    throw err;
}

// Register event listeners
$(window).load(function () {
    try
    {
        requestRegistersTable();
        $('#device-dropdown').change(requestRegistersTable);
        $('#tag-dropdown').change(requestRegistersTable);
        $('#not-tag-dropdown').change(requestRegistersTable);
        $('#add-reg-name-dropdown').change(requestRegistersTable);
        $('#expand-checkbox').change(requestRegistersTable);
    }
    catch(err)
    {
        handleError(err)
    }
});