function hide_element_by_class(element_class) {
  let ip_element_class = '.' + element_class;
  $(ip_element_class).hide();
}

function show_element_by_class(element_class) {
  let ip_element_class = '.' + element_class;
  $(ip_element_class).show();
}

// add row with self delete button to table
function append_showtime_detail_row_to_table(table_id, number_of_screen, uuid) {
  let ip_table_id = "#" + table_id;

  row = '<tr class="showtime_row">';
  row += '<td>';
  row += '<input id="showtime_{0}" name="showtime" class="form-control wrapper" style="width: 100%;"/>'.f(uuid);
  row += "<script>create_time_picker('showtime_{0}');</script>".f(uuid);
  row += '</td>';
  row += '<td>';
  row += '<input id="end_time_{0}" type="text" class="form-control wrapper" readonly></input>'.f(uuid);
  row += '</td>';
  row += '<td>';
  row += '<select id="mv_id_{0}" name="mv_id" class="form-control wrapper" style="width: 100%;" onchange="create_select_option_arr_of_dict({1}, {2}, {3}, movie_format_map[{4}]);" required>'.f(uuid, "'mv_format_{0}'", "'format_strshortname'", "'format_strcode'", "this.value");
  row += "<script>copy_option_of_datalist_to_select_element('mv_id_{0}', 'mv_list_options');</script>".f(uuid);
  row += '</select>';
  row += "<script>make_select_searchable('mv_id_{0}');</script>".f(uuid);
  row += '</td>';
  row += '<td>';
  row += '<select id="mv_format_{0}" name="mv_format" class="form-control wrapper" style="width: 100%;" required></select>'.f(uuid);
  row += "<script>create_select_option_arr_of_dict('mv_format_{0}', 'format_strshortname', 'format_strcode', movie_format_map[$('#mv_id_{0}').val()]);</script>".f(uuid);
  row += '</td>';
  row += '<td>';
  row += '<select id="lang_{0}" name="lang" class="form-control wrapper" style="width: 100%;" required>'.f(uuid);
  row += "<script>copy_option_of_datalist_to_select_element('lang_{0}', 'lang_options');</script>".f(uuid);
  row += '</select>';
  row += "<script>make_select_searchable('lang_{0}');</script>".f(uuid);
  row += '</td>';
  row += '<td>';
  row += '<i class="fas fa-minus-circle fa-2x cursor_hand" style="color: red; margin-left: .2em;" onclick="remove_element($(this).parent().parent());"></i>';
  row += '<input type="text" name="screen" value="{0}" hidden/>'.f(number_of_screen);
  row += '</td>';
  row += '</tr>';

  row += '<script>';
  row += '$("#mv_id_{0}, #showtime_{0}").on("change", function(){ set_value_to_element("end_time_{0}", calculate_firm_ending_time($("#showtime_{0}").val(), $("#mv_id_{0} option:selected").text().substring($("#mv_id_{0} option:selected").text().lastIndexOf("(")+1, $("#mv_id_{0} option:selected").text().lastIndexOf(" "))) ) });'.f(uuid);
  row += '</script>';

  $(ip_table_id + " > tbody:last").append(row);
}

function copy_showtime_by_screen_table_id(screen_table_id) {
  $("#temp_id_of_screen_table_to_copy").val(screen_table_id).change();
}

function paste_showtime_to_screen_table_id(to_screen_table_id, screen_number) {
  let from_screen_table_id = '#' + $('#temp_id_of_screen_table_to_copy').val();
  $('#' + to_screen_table_id).find('.showtime_row').remove();

  let uuid;
  $(from_screen_table_id).find("[name='showtime']").each(function (index, el) {
    uuid = createUUID();
    append_showtime_detail_row_to_table(to_screen_table_id, screen_number, uuid);
    set_value_to_element('showtime_' + uuid, el.value);
    set_value_to_element('mv_id_' + uuid, $(from_screen_table_id).find("[name='mv_id']")[index].value);
    set_value_to_element('mv_format_' + uuid, $(from_screen_table_id).find("[name='mv_format']")[index].value);
    set_value_to_element('lang_' + uuid, $(from_screen_table_id).find("[name='lang']")[index].value);
  });

  $("#temp_id_of_screen_table_to_copy").val('').change();
}

function calculate_firm_ending_time(start_time, end_time_min) {
  start_time_split = start_time.split(':');
  temp_start_h = parseInt(start_time_split[0]);
  temp_start_m = parseInt(start_time_split[1]);
  end_time_min = parseInt(end_time_min);

  let hours = (end_time_min + temp_start_m) / 60;
  let real_hours = Math.floor(hours);
  let minutes = (hours - real_hours) * 60;
  let real_minutes = Math.round(minutes);

  real_hours += temp_start_h;

  if (real_hours > 23) {
    real_hours = (real_hours - 4).toString();
    real_hours = '0' + real_hours.substring(1);
  }

  if (real_minutes < 10){
    real_minutes = '0' + real_minutes.toString();
  }

  return "{0}:{1}".f(real_hours, real_minutes)
}