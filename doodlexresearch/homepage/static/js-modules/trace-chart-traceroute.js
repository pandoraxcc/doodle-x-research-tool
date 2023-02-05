
// Instances used for creating the charts

var chart_instance_ping = null;
var charts_instance_countries = null;
var charts_instance_organizations = null;
var charts_instance_adresses = null;

// Colors for the pie charts
var color_palete_countries = [
  "#472183",
  "#4B56D2",
  "#82C3EC",
  "#47B5FF",
  "#413C69",
  "#4A47A3",
  "#A7C5EB"
];

var color_palete_organizations = [
  "#242F9B",
  "#646FD4",
  "#9BA3EB",
  "#4C3F91",
  "#9145B6",
  "#B958A5",
  "#FF5677"
];

var color_palete_adresses = [
  "#4B4A5A",
  "#A10054",
  "#2D31FA",
  "#EA168E"
];

function clear_chart(chart_instance) {
   if(chart_instance != null) {
     chart_instance.destroy();
   }
}

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

    clear_chart(chart_instance_ping);

    // Building diagramm
    chart_instance_ping = new Chart(ctx, {
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
        if (location_dict['country'] !== null) {
          countries.push(location_dict['country']);
        }
      }
    })

    // Adding the header for the chart 
    if ($(".countries-title").length === 0) {
      $(".country-graph").prepend(`<h3 class="countries-title mx-auto p-3">Packet and countries</h3>`);
    }

    // Summary for each country
    var country_counts = _.countBy(countries);

    clear_chart(charts_instance_countries);

    // Building the chart
    charts_instance_countries = new Chart(ctx1, {
      type: "pie",
      data: {
        labels: Object.keys(country_counts),
        datasets: [{
          label: 'Countries',
          backgroundColor: color_palete_countries,
          data: Object.values(country_counts)
        }]

      },
      options: {
        responsive: true
      }
    });
  }
}

export function display_organization_chart(data, ctx2) {

  var organizations = [];
  var organizations_counts;

  if (data.length >= 1) {
    $.each(data, function (index, geo_details) {
      if (typeof (geo_details[5]) == 'object') {
        var location_dict = geo_details[5];
        if (location_dict['organization'] !== null) {
          organizations.push(location_dict['organization']);
        }
      }
    })

    // Adding the header for the chart 
    if ($(".organizations-title").length === 0) {
      $(".organization-graph").prepend(`<h3 class="organizations-title mx-auto p-3">Packet and organizations</h3>`);
    }

    // Summary for each organization
    var organizations_counts = _.countBy(organizations);
    console.log(organizations);
    console.log(organizations_counts);

    clear_chart(charts_instance_organizations);

    // Building the chart
    charts_instance_organizations = new Chart(ctx2, {
      type: "bar",
      data: {
        labels: Object.keys(organizations_counts),
        datasets: [{
          backgroundColor: color_palete_organizations,
          data: Object.values(organizations_counts)
        }]

      },
      options: {
        legend: { display: false },
        responsive: true,
      }
    });

  }
}

export function display_adress_chart(data, ctx3) {
  var adresses = [];
  var count_adresses;

  if (data.length >= 1) {
    $.each(data, function (index, hop_array) {
      adresses.push(hop_array[4]);
    })
    console.log(adresses);

    // Adding the header for the chart 
    if ($(".adress-title").length === 0) {
      $(".adresses-graph").prepend(`<h3 class="adress-title mx-auto p-3">Types of adressess</h3>`);
    }

    // Summary for each organization
    var count_adresses = _.countBy(adresses);
    console.log(count_adresses);

    clear_chart(charts_instance_adresses);

    // Building the chart
    charts_instance_adresses = new Chart(ctx3, {
      type: "bar",
      data: {
        labels: Object.keys(count_adresses),
        datasets: [{
          backgroundColor: color_palete_adresses,
          data: Object.values(count_adresses)
        }]

      },
      options: {
        legend: { display: false },
        responsive: true,
      }
    });
  }
}
