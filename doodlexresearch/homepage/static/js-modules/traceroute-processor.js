
import * as graphs from "./trace-chart-traceroute.js"

// Used for storing the arrays of traceroute data
var trace_array;

// Canvas and ctx for drawing the ping chart
var canvas = document.getElementById("pings");
const ctx = canvas.getContext('2d');

// Canvas and ctx for drawing the countries chart
var canvas1 = document.getElementById("countries");
const ctx1 = canvas1.getContext('2d');

// Canvas and ctx for drawing the organizations chart
var canvas2 = document.getElementById("organizations");
const ctx2 = canvas2.getContext('2d');

// Canvas and ctx for drawing the organizations chart
var canvas3 = document.getElementById("adresses");
const ctx3 = canvas3.getContext('2d');

// Table blueprint to upload the data 
var table_headers = `
        <div class="container mx-auto" style="padding: 1rem 0rem;">
            <h3 class="text-center p-3">Traceroute Stats</h3>
            <table class="table table-striped text-center">
                <thead>
                    <tr>
                        <th>Hop number</th>
                        <th>Host name</th>
                        <th>Ip adress</th>
                        <th>Ping</th>
                        <th>Type of adress</th>
                        <th>Location and organization</th>
                    </tr>
                </thead>
                <tbody class="data-rows">
                </tbody>
            </table>
        </div>
`

// Blueprint for verification
function validate_input(target_ip) {
    if (target_ip.length > 1) {
        return target_ip;
    }
    else {
        return false;
    }
}

function setup_after_request() {
    // removing the spinner and status 
    $(".traceroute-results").empty();
    // the data is ready and another request could be sumbitted
    $(".traceroute-load").prop("disabled", false);
    $(".input-traceroute").prop("disabled", false);

    

}

function setup_on_request(target_ip) {
    // on the first launch, slide the image
    $(".traceroute-image").slideUp(700);
    // removing the results table with the header 
    $(".traceroute-results").empty();
    // hiding the charts
    hide_charts();
    // adding the status bar and the loader
    $(".traceroute-results").append(
        `<p style="margin-top: 3rem;" class="text-center loading-info">Please wait, while we performing traceroute to ${target_ip}</p>
        <img style="display:block;" class="mx-auto loading-spinner" src="/static/img/traceroute/loading-animation.webp" alt="" width="8%">`);
    // Prevent another submission while executing
    $(".traceroute-load").prop("disabled", true);
    $(".input-traceroute").prop("disabled", true);

}

function display_data(array) {
    // inserted the empty table with 5 columns
    $(".traceroute-results").append(table_headers);

    // getting the single array with data
    $.each(array, function (index, items) {
        $(".data-rows").append(`<tr></tr>`);

        $.each(items, function (index, item) {
            if (typeof (item) == 'string') {
                $("tr:last").append(`<td class="align-middle">${item}</td>`);
            }

            // get location data
            if (typeof (item) == 'object') {
                var location_inf = ``;

                for (var key in item) {
                    location_inf += `${key}: ${item[key]}</br>`;

                }

                $("tr:last").append(`<td class="align-middle">${location_inf}</td>`);

            }
        })
    })

}

function hide_charts() {
    $(".graphs").hide();
}

function show_charts() {
    $(".graphs").show();
}

function process_submission() {
    var target_ip = $("#ip_addr").val();
    var validation = validate_input(target_ip);

    if (validation) {

        setup_on_request(target_ip);

        // POST request

        $.ajax({

            type: "post",
            data: { ip: target_ip },

            success: function (data) {
                console.log(data)
                // Converting from JSON string to the array
                trace_array = JSON.parse(data);
                console.log("Got the response from the server:");
                console.log(trace_array);

                // Show the charts
                show_charts();
                // Modify the dom
                setup_after_request();
                // Append the table with the data
                display_data(trace_array);

            },

            error: function () {
                console.log("No response from the server");
            }
        })
    }

}

/* On load wait for the submit button */

$(document).ready(function () {

    // hiding on the first load
    hide_charts();

    $(".traceroute-load").click(process_submission());
    $(".input-traceroute").keypress(function(e) {
        if(e.key === "Enter") {
            console.log("enter pressed")
            process_submission();
        }
    })

})


$(document).ajaxComplete(function () {
    graphs.display_ping_chart(trace_array, ctx);
    graphs.display_country_chart(trace_array, ctx1);
    graphs.display_organization_chart(trace_array, ctx2);
    graphs.display_adress_chart(trace_array, ctx3);
    console.log("Finished the task");
});