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

    var registersTableRequester = new RegistersTableRequester();
    registersTableRequester.setDevice($("#devices").val());
    registersTableRequester.setTags($("#tags").val());
    registersTableRequester.setNotTags($("#not-tags").val());
    registersTableRequester.setRegNames($("#add-reg-names").val());
    registersTableRequester.setRegAddrs($("#add-regs").val());
    registersTableRequester.setExpand($("#expand_addresses").val());
    registersTableRequester.setFields($("#fields").val());
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
    }
    catch(err)
    {
        handleError(err)
    }
});