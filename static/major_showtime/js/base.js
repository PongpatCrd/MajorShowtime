String.prototype.format = String.prototype.f = function() {
  var s = this,
      i = arguments.length;

  while (i--) {
      s = s.replace(new RegExp('\\{' + i + '\\}', 'gm'), arguments[i]);
  }
  return s;
};

function createUUID() {
  return 'xxxxxxxx-xxxx-4xxx-yxxx-xxxxxxxxxxxx'.replace(/[xy]/g, function(c) {
  var r = Math.random() * 16 | 0, v = c == 'x' ? r : (r & 0x3 | 0x8);
  return v.toString(16);
  });
}

// loading screen
function loading_screen(turn_on){
  if(turn_on){
    $('#loading_screen').show();
  }
  else{
    $('#loading_screen').hide();
  }
}

$(document).on('submit', function(){
  loading_screen(true);
});

$(document).ready(function(){
  loading_screen(false);
});

// create options in select element  id given
function create_number_select_option(select_element_id, start, stop, step){
  let select_element = "#" + select_element_id;
  let temp_option;
  if(start < stop){
    // forward
    for(let i=start; i<=stop; i+=step){
      temp_option = '<option value=';
      temp_option += '"' + i + '"';
      temp_option += ' label=';
      temp_option += '"' + i + '"';
      temp_option += "</option>";
      $(select_element).append(temp_option);
    }
  }
  else{
    // backward
    for(let i=start; i>=stop; i-=step){
      temp_option = '<option value=';
      temp_option += '"' + i + '"';
      temp_option += ' label=';
      temp_option += '"' + i + '"';
      temp_option += "</option>";
      $(select_element).append(temp_option);
    }
  }
}

// sub-string for last page number of pagination
function get_last_page_of_paginator(output_element_id, paginator_safe_string){
  // paginator_safe_string = {{ "something|safe" }}
  let element_id = "#" + output_element_id;
  let last_page = paginator_safe_string.split(" ")[3].replace(">", "");

  $(element_id).html(last_page);
}

// set default value of each input in home from parameters from url (prevent sent that parameters from backend)
function set_default_input_params_from_url(){
  let search_params = new URLSearchParams(window.location.search);
  let temp_element;
  for(let detail of search_params){
    temp_element = "#" + detail[0];
    $(temp_element).val(detail[1]);
  }
}

// set value to input element id
function set_value_to_element(element_id, value){
  let ip_element_id = "#" + element_id;
  $(ip_element_id).val(value).change();
}

// set datepicker value
function set_datepicker_value_dy_self_init(element_id){
  // self element value must in format dd/nn/yyyy
  let ip_element_id = "#" + element_id;
  $(ip_element_id).datepicker('setDate',  $(ip_element_id).val());
}

// set selected option by input given
function set_selected_to_option_in_select_element(select_element_id, in_value){
  let ip_select_element_id = "#" + select_element_id;
  $(ip_select_element_id).find('option:selected').attr('selected', false);
  $(ip_select_element_id).find('option[value="' + in_value + '"]').attr('selected', true);
}

// copy value from one element to another one element
function copy_value(source_element_id, destination_element_id){
  let s_element_id = "#" + source_element_id;
  let d_element_id = "#" + destination_element_id;
  $(d_element_id).val($(s_element_id).val());
}

// copy all option in datalist to select element id given
function copy_option_of_datalist_to_select_element(select_element_id, datalist_id){
  let ip_select_element_id = "#" + select_element_id;
  let ip_datalist_id = "#" + datalist_id;
  $(ip_select_element_id).html($(ip_datalist_id).html());
}

// copy prop value
function copy_prop_value(source_element_id, destination_element_id, prop_name){
  let s_element_id = "#" + source_element_id;
  let d_element_id = "#" + destination_element_id;
  $(d_element_id).prop(prop_name, $(s_element_id).prop(prop_name));
}

// error modal
function set_alert_error(error_msg){
  $("#error_msg").text(error_msg);
  if($.trim($("#error_msg").text()) == ""){
    $("#error_alert").prop("hidden", true);
  }
  else{
    $("#error_alert").prop("hidden", false);
  }
}

// plug-in select2 to element by id (make select searchable)
function make_select_searchable(element_id){
  let ip_element_id = "#" + element_id;
  $(ip_element_id).select2({theme: "bootstrap4"});
}

// plug-in select2 to element by id (make select searchable)
function make_select_searchable_multiple(element_id){
  let ip_element_id = "#" + element_id;
  $(ip_element_id).select2({multiple: true, theme: "bootstrap4"});
}

// make input type text to datepicker
function make_input_to_datepicker(element_id){
  let ip_element_id = "#" + element_id;
  $(ip_element_id).datepicker({
    dateFormat: 'dd-mm-yy'
  });
  $(ip_element_id).attr( 'readOnly' , 'true' );
}

// make input type text to datepicker
function make_input_to_datepicker_disabled_past(element_id){
  let ip_element_id = "#" + element_id;
  $(ip_element_id).datepicker({
    dateFormat: 'dd-mm-yy',
    minDate: -7
  });
  $(ip_element_id).attr( 'readOnly' , 'true' );
}

// reset input in form
function reset_form_input(form_id){
  let ip_form_id = "#" + form_id;
  $(ip_form_id).trigger('reset');
}

// clear all default value in form
function clean_init_value_of_form(form_id){
  let ip_form_id = "#" + form_id;
  $(ip_form_id).find('input:not([type="hidden"])').val('');
  $(ip_form_id).find('select').prop('selectedIndex', 0).change();
}

// check all input in form if not any empty allow button to submit
function allow_submit_button_if_form_complete(form_id, button_id){
  let ip_form_id = "#" + form_id;
  let ip_button_id = "#" + button_id;

  let empty = $(ip_form_id).find('input:required, select:required').filter(function() {
    return this.value === "";
  });
  if(empty.length) {
    $(ip_button_id).removeClass().addClass('btn btn-light cursor_default');
    $(ip_button_id).prop('disabled', true);
  }
  else{
    $(ip_button_id).removeClass().addClass('btn btn-info cursor_hand');
    $(ip_button_id).prop('disabled', false);
  }
}

// remove and add class
function remove_all_class_and_add_new_class(element_id, class_str){
  let ip_element_id = '#' + element_id;
  $(ip_element_id).removeClass().addClass(class_str);
}

// set inner html from value given
function set_inner_html_from_value_given(element_id, value_given){
  let ip_element_id = '#' + element_id;
  $(ip_element_id).html(value_given);
}

// create time_picker
function create_time_picker(element_id){
  let ip_element_id = '#' + element_id;
  
  $(ip_element_id).prop('readOnly', true);
  let timepicker = $(ip_element_id).timepicker({
    mode: '24hr',
    format: 'HH:MM',
    uiLibrary: 'bootstrap4'
  });
  return timepicker;
}

// remove element
function remove_element(element){
  $(element).remove();
}

// add div with hidden input contain inside to parent element given
function add_div_of_hidden_input_tag_to_element(element_id, hidden_input_name, in_value){
  let ip_element_id = '#' + element_id;
  let remove_button = "<i class='fas fa-minus-circle cursor_hand' style='color: red;' onclick='remove_element($(this).parent());'></i>";
  
  $(ip_element_id).append(
    "<div><input name='{0}' value='{1}' hidden/>{2} {3}</div>".f(hidden_input_name, in_value, in_value, remove_button)
  );
}

// add div with hidden input contain inside to parent element given
function add_div_of_hidden_input_tag_to_element_arr(element_id, hidden_input_name, in_value_arr){
  for(in_value of in_value_arr){
    add_div_of_hidden_input_tag_to_element(element_id, hidden_input_name, in_value);
  }
}

// create option to select element from array of dict given
function create_select_option_arr_of_dict(element_id, key_label, key_value, arr_of_dict){
  let ip_element_id = "#" + element_id;
  let options_txt = "";
  for(i in arr_of_dict){
    options_txt += "<option value='{0}'>{1}</option>\n".f(arr_of_dict[i][key_value], arr_of_dict[i][key_label]);
  }
  $(ip_element_id).html(options_txt);
}

function change_values_by_class(element_class, in_value){
  let ip_element_class = "." + element_class;
  $(ip_element_class).val(in_value);
}

function set_value_of_input_in_some_element_by_name(parent_element_id, input_name, in_value){
  let ip_parent_element_id = '#' + parent_element_id;
  let ip_input_name = '[name="{0}"]'.f(input_name);
  $(ip_parent_element_id).find(ip_input_name).val(in_value);
}

function check_element_has_value(element_id){
  let ip_element_id = '#' + element_id;

  console.log($(ip_element_id).val());
}