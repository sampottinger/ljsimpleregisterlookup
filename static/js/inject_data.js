var displayingInputControls = false;


$(window).load(function () {
    $('#catchphrase').hide().delay(200).slideDown();
    $('#input-section #controls').hide();
    
    $('#input-code-area').bind("keyup", function(e) {                          
        if ($('#input-code-area').val() == '') {
            if (displayingInputControls) {
                $('#input-section #controls').fadeOut(function () {
                    $('#input-section #title').fadeIn();
                });
            }
            displayingInputControls = false;
        } else {
            if (!displayingInputControls) {
                $('#input-section #title').fadeOut(function () {
                    $('#input-section #controls').fadeIn();
                });
            }
            displayingInputControls = true;
        }
    });

    $('#generate-button').click(function () {
        $('#input-section #controls').fadeOut(function () {
            $('#input-section #waiting').fadeIn();

            $.ajax({
                type: "POST",
                url: "/scribe",
                data: { input: $('#input-code-area').val() }
            }).done(function( msg ) {
                $('#output-code-area').html(msg);
                $('#output-section').slideDown();
                $('#input-section #waiting').hide();
                $('#input-section #controls').fadeIn();
            });
        });
    });
});
