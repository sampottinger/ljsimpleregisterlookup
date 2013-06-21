var URL_TEMPLATE = 'http://ljsimpleregisterlookup.herokuapp.com/lookup.html' +
    '?device_name={{device_name}}'+
    '&tags={{tags}}'+
    '&expand-addresses={{expand-addresses}}'+
    '&fields={{fields}}'

var FRAME_TEMPLATE = '<iframe width="850" height="400" src="{{&url}}">' +
    '</iframe>';

// Register event listeners
$(window).load(function () {
    $('#export-button').click(function()
    {
        var deviceName = encodeURIComponent($("#device-dropdown").val());
        var tags = encodeURIComponent($("#tag-dropdown").val());
        var expandAddresses = $("#expand-checkbox").is(':checked');

        var fields = ["name", "address"];

        if($("#type-check").is(":checked"))
            fields.push("type");

        if($("#fwmin-check").is(":checked"))
            fields.push("fwmin");

        if($("#rw-check").is(":checked"))
            fields.push("rw");

        if($("#tags-check").is(":checked"))
            fields.push("tags");

        if($("#default-check").is(":checked"))
            fields.push("default");

        fields.push("description");

        var data = {
            "device_name": deviceName,
            "tags": tags,
            "expand-addresses": expandAddresses,
            "fields": fields.join(",")
        };

        var url = Mustache.render(URL_TEMPLATE, data);
        var code = Mustache.render(FRAME_TEMPLATE, {"url": url});

        $("#export-code-holder").val(code);
    });
});