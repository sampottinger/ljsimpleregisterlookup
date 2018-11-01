        $( document ).ready(function() {
 
        var urlParams = new URLSearchParams(window.location.search);
        var Device = urlParams.get('Device'); 
        var DevicesTag = urlParams.get('Tag'); 
        var TagsExpand = urlParams.get('Expand'); 
        var deviceDropdown = document.getElementById('device-dropdown');
        var len = deviceDropdown.options.length;
        for(i = 0; i < len; i++)
         {
         if (deviceDropdown.options[i].innerHTML === Device)
         {
         deviceDropdown.selectedIndex = i;
         break;
         }     
        }
        var tagdropdown = document.getElementById('tag-dropdown');
        var len = tagdropdown.options.length;
        for(i = 0; i < len; i++)
         {
         if (tagdropdown.options[i].innerHTML === DevicesTag)
         {
         tagdropdown.selectedIndex = i;
         break;
         }     
        }
        if(TagsExpand === "true"){
            document.getElementById("expand-checkbox").checked = true;
        }
        });
         $('#device-dropdown').on('change', function() {
            deeplink();
        });
          $('#tag-dropdown').on('change', function() {
            deeplink();
        });
           $('#expand-checkbox').on('change', function() {
            deeplink();
        });
            function deeplink(){
            var newurl = window.location.protocol + "//" + window.location.host + window.location.pathname + "?Device=" + $("#device-dropdown").val() + "&Tag=" + $("#tag-dropdown").val() + "&Expand=" + $("#expand-checkbox").is(':checked')
            window.history.pushState({ path: newurl }, '', newurl);
            }
