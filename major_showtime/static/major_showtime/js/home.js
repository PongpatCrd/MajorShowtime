// create dashboard of movies admis from formatted dataset
function create_line_chart(element_id, dataset, title){
  let new_chart = new Chart(document.getElementById(element_id), {
    type: 'line',
    data: dataset,
    options: {
      responsive: true,
      title: {
        display: true,
        text   : title
      },
      scales: {
        yAxes: [{
          ticks: {
            precision: 0,
          }
        }],
      },
    }
  });

  return new_chart
}

// set button hide/show all to hidden/show all line of chart
function set_hide_show_all_lines_button(button_id, chart){
  let button_name = '#' + button_id;
  $(button_name).on('click', function(){
    chart.data.datasets.forEach(function(e) {
      e.hidden = !e.hidden;
    });
    chart.update();
  });
}