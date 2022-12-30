
/* On load wait for the submit button */


$(document).ready(function() {
    $(".traceroute-load").click(
        function() {
            var target_ip = $("#ip_addr").val();

            if (test_domain(target_ip) == true) {
                console.log("true");
                $(".traceroute-image").slideUp(700);
                $(".traceroute-results").append(
                    `<p class="text-center">Please wait, while we performing traceroute to ${target_ip}</p>
                    <img style="display:block;" class="mx-auto" src="/static/img/traceroute/loading-animation.webp" alt="" width="8%">`);
                //console.log("jquery is working");
            }

    
        }
    )
})
