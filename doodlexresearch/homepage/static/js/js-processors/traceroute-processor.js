
/* On load wait for the submit button */

$(document).ready(function () {

    // Used for storing the arrays of traceroute data

    var trace_array;

    var table_headers = `
    <div class="container mx-auto" style="padding: 1rem 0rem;">
        <h3 class="text-center p-3">Results</h3>
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

    function validate_json(data){
        console.log("was here111");
        try {
            JSON.parse(data);
            return true;
        }
        catch (error) {
            return false;
        }
    }

    function after_trace(target_ip) {
        // $(".traceroute-results").remove(".loading-spinner", ".loading-info");
        $(".traceroute-results").empty();
        $(".traceroute-load").prop("disabled", false);

    }

    function before_trace(target_ip) {
        $(".traceroute-results").empty();
        $(".traceroute-results").append(
            `<p class="text-center loading-info">Please wait, while we performing traceroute to ${target_ip}</p>
            <img style="display:block;" class="mx-auto loading-spinner" src="/static/img/traceroute/loading-animation.webp" alt="" width="8%">`);

        // Prevent another submission while executing
        $(".traceroute-load").prop("disabled", true);
    }

    function display_data(array) {
        // inserted the empty table with 5 columns
        $(".traceroute-results").append(table_headers);
    
        // getting the single array with data
        $.each(array, function(index, items){
            $(".data-rows").append(`<tr></tr>`);

            $.each(items, function(index, item){
                if (typeof(item) == 'string') {
                    $("tr:last").append(`<td class="align-middle">${item}</td>`);
                }

                // we get our location data
                if (typeof(item) == 'object') {
                    var location_inf = ``;

                    for (key in item) {
                        location_inf += `${key}: ${item[key]}</br>`;

                    }

                    $("tr:last").append(`<td class="align-middle">${location_inf}</td>`);

                }
            })
        })

        }


    $(".traceroute-load").click(
        function () {
            var target_ip = $("#ip_addr").val();
            var validation = validate_input(target_ip);

            if (validation) {

                $(".traceroute-image").slideUp(700);
                before_trace(target_ip);
                

                // POST request

                $.ajax({

                    type: "post",
                    data: { ip: target_ip },

                    success: function (data) {

                        // Converting from JSON string to the array
                        trace_array = JSON.parse(data);
                        console.log(trace_array);


                        /* Changing the dom elements */
                        after_trace(target_ip);
                        display_data(trace_array);

                    },

                    error: function () {
                        console.log("doesn't work");
                    }
                })
            }

        }
    )
})