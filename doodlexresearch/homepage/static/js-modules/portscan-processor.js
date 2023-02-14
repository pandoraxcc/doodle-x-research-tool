import * as check_vulnerability from "./protscan-vuln-check.js"


// Table blueprint to upload the data 
var table_ports = `
        <div>
            <div class="container mx-auto" style="padding: 1rem 0rem;">
                <h3 class="text-center p-3"> Scan Results</h3>
                <table class="table text-center">
                    <thead>
                        <tr>
                            <th>Port number</th>
                            <th>Host name</th>
                            <th>Status</th>
                        </tr>
                    </thead>
                    <tbody class="data-rows">
                    </tbody>
                </table>
            </div>
        </div>
`
function setup_after_request() {
    // removing the spinner and status 
    $(".portscan-results").empty();
    // the data is ready and another request could be sumbitted
    $(".scanports").prop("disabled", false);

}

function validate_port_fields(adress, range1, range2 ) {

    // if the user wants to scan a single port, assign the value of range1 to 0

    if(adress.length > 1) {

        if (range2 > range1 && range2 >= 1 && range2 <= 65535) {

            // in case there are errors from the previous submissions
            
            $("input").removeClass("is-invalid");
            $(".invalid-feedback").remove();
            return true

        }

        else {
            console.log(range2)
            console.log(range1)
            $(".invalid-feedback").remove();
            $("#end-port").addClass("is-invalid");
            $(".end-port").append(`<div class="invalid-feedback">Max 65535 or higher than from port</div>`);
        }
    }
    
    else {
        console.log("error");
        $("#addr").addClass("is-invalid");
        $(".ip-addr").append(`<div class="invalid-feedback">Enter valid adress</div>`);

    }
}

function setup_on_request() {
    // on the first launch, slide the image
    $(".portscan-image").slideUp(700);
    // adding the status bar and the loader
    $(".portscan-results").empty()
    $(".portscan-results").append(
        `<p style="margin-top: 3rem;" class="text-center loading-info">Please wait, while we performing port scan</p>
        <img style="display:block;" class="mx-auto loading-spinner" src="/static/img/traceroute/loading-animation.webp" alt="" width="8%">`);
    // Prevent another submission while executing
    $(".scanports").prop("disabled", true);
}

function display_data(array) {
    // inserted the empty table with 5 columns
    $(".portscan-results").append(table_ports);
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

$(document).ready(function() {
    $(".scanports").click(
        function(){
            var addr = $("#addr").val()
            var from_port = $("#from-port").val();
            var end_port = $("#end-port").val();

            if(from_port==""){
                from_port = 0;
            }
            
            if(validate_port_fields(addr,from_port,end_port)){

                setup_on_request();

                // POST request

                $.ajax({

                    type: "post",
                    data: { host: addr, fromport: from_port, endport: end_port },

                    success: function (data) {

                        // Converting from JSON string to the array

                        var ports_info = JSON.parse(data);
                        setup_after_request();

                        display_data(ports_info);
                        check_vulnerability.check_if_ports_vulnerable(ports_info);


                    },

                    error: function () {
                        console.log("No response from the server");
                    }
                })
            };
        }
    );
})
