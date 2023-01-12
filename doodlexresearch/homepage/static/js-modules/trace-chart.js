
// Colors for the pie charts
var color_palete = [
  "#472183",
  "#4B56D2",
  "#82C3EC",
  "#F1F6F5",
  "#256D85",
  "#47B5FF",
  "#DFF6FF",
  "#413C69",
  "#4A47A3",
  "#709FB0",
  "#A7C5EB"
];

export function display_ping_chart(data, ctx) {

  if (data.length >= 1) {

    var pings = [];

    $.each(data, function (index, hop_array) {
      if (hop_array[3] != "none") {
        pings.push(hop_array[3]);
      }
      else {
        pings.push("0");
      }
    })


    // Adding the header for the chart 
    if ($(".ping-title").length === 0) {
      $(".ping-graph").prepend(`<h3 class="ping-title mx-auto p-3">Ping Graphs</h3>`);
    }

    // Building diagramm
    var chart_instance_ping = new Chart(ctx, {
      type: 'line',
      data: {
        // getting the list of hops, starting from 1 to pings.length
        labels: Array.from({ length: pings.length }, (_, i) => i + 1),
        datasets: [{
          label: 'Ping dinamics from each network switch',
          data: pings,
          borderWidth: 1,
          borderColor: "#255fc5"
        }]
      },
      options: {
        scales: {
          y: {
            beginAtZero: true
          }
        },
        responsive: true
      }
    });

  }

}

export function display_country_chart(data, ctx1) {

  var countries = [];
  var country_counts;

  if (data.length >= 1) {
    $.each(data, function (index, geo_details) {
      if (typeof (geo_details[5]) == 'object') {
        var location_dict = geo_details[5];
        countries.push(location_dict['country']);
      }
    })

    // Adding the header for the chart 
    if ($(".countries-title").length === 0) {
      $(".country-graph").prepend(`<h3 class="countries-title mx-auto p-3">Packet and countries</h3>`);
    }

    // Summary for each country
    var country_counts = _.countBy(countries);

    // Building the chart
    var charts_instance_countries = new Chart(ctx1, {
      type: "pie",
      data: {
        labels: Object.keys(country_counts),
        datasets: [{
          label: 'Countries',
          backgroundColor: color_palete,
          data: Object.values(country_counts)
        }]

      },
      options: {
        responsive: true
      }
    });
  }
}

export function display_organization_chart(data) {
  // index 4 for the countries as the object
  // object {city, country, country_area, organization, region}
}