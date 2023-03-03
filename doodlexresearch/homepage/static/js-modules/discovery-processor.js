// Table blueprint to upload the data 
var discovery_scan = `
            <div class="container mx-auto" style="padding: 1rem 0rem;">
                <h3 class="text-center p-3 mx-auto">Scan Results</h3>
                <table class="table text-center">
                    <thead>
                        <tr>
                            <th>Ip adress</th>
                            <th>Status</th>
                            <th>Connection identified by</th>
                        </tr>
                    </thead>
                    <tbody class="data-rows">
                    </tbody>
                </table>
            </div>
`

function display_data(array) {
    // inserted the empty table with 2 columns
    $(".network-discovery-results").append(discovery_scan);
        // getting the single array with data
    $.each(array, function (index, items) {
        $(".data-rows").append(`<tr></tr>`);

        $.each(items, function (index, item) {
            if (typeof (item) == 'string') {
                $("tr:last").append(`<td class="align-middle">${item}</td>`);
            }
        })


    })
}

function setup_after_request() {
    // removing the spinner and status 
    $(".network-discovery-results").empty();
    // the data is ready and another request could be sumbitted
    $(".discovery-load").prop("disabled", false);

}

function setup_on_request() {
    // on the first launch, slide the image
    $(".discovery-image").slideUp(700);
    // adding the status bar and the loader
    $(".network-discovery-results").empty()
    $(".network-discovery-results").append(
        `<p style="margin-top: 3rem;" class="text-center loading-info">Please wait, while we are performing netwrok discovery</p>
        <img style="display:block;" class="mx-auto loading-spinner" src="/static/img/traceroute/loading-animation.webp" alt="" width="8%">`);
    // Prevent another submission while executing
    $(".discovery-load").prop("disabled", true);
}

function validate_input(netmask) {
    if (netmask.length > 1) {
        return true;
    }
    else {
        return false;
    }
}

$(document).ready(function() {

    $(".discovery-load").click(
        
        function(){

            var netmask = $("#network_ip").val();

            if(validate_input(netmask)) {
                
                setup_on_request()

                // POST request

                $.ajax({

                    type: "post",
                    data: { host: netmask },

                    success: function (data) {

                        // Converting from JSON string to the array

                        var discovery_info = JSON.parse(data);
                        setup_after_request()
                        display_data(discovery_info)
                    },

                    error: function () {
                        console.log("No response from the server");
                    }
                })

            }
        })
});