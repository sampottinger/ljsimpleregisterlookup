/**
 * Javascript client-side controller for Simple Register Lookup.
 *
 * Client-side controller for the Simple Register Lookup, a web-based modbus
 * map lookup utility.
 *
 * @author Sam Pottinger
 * @license GNU GPL v2
**/


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

function requestRegistersTable()
{
    $('#loading-image').show();
    var registersTableRequester = new RegistersTableRequester();
    registersTableRequester.setDevice($("#device-dropdown").val());
    registersTableRequester.setTags($("#tag-dropdown").val());
    registersTableRequester.setNotTags($("#not-tag-dropdown").val());
    registersTableRequester.setRegNames($("#add-reg-name-dropdown").val());
    registersTableRequester.setExpand($("#expand-checkbox").is(':checked'));
    registersTableRequester.loadTable(
        'register-table-container',
        function() { $('#loading-image').hide(); }
    );
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