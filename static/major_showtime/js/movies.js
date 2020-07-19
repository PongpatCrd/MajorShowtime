// change icon of checkbox in tag <i> base on input element id
function change_checkbox_icon_base_on_element_value(input_element_id, icon_element_id){
  let ip_element_id = "#" + input_element_id;
  let ic_element_id = "#" + icon_element_id;

  if($(ip_element_id).val() == "1"){
    $(ic_element_id).removeClass("fas fa-square");
    $(ic_element_id).removeClass("fas fa-check-square");
    $(ic_element_id).addClass("fas fa-check-square");
  }
  else if($(ip_element_id).val() == "0"){
    $(ic_element_id).removeClass("fas fa-square");
    $(ic_element_id).removeClass("fas fa-check-square");
    $(ic_element_id).addClass("fas fa-square");
  }
}

function uncheck_all_checkbox_icon(icon_element_class){
  let ic_element_class = "." + icon_element_class;

  $(ic_element_class).removeClass("fas fa-check-square");
  $(ic_element_class).removeClass("fas fa-square");
  $(ic_element_class).addClass("fas fa-square");
}

function check_all_checkbox_icon(icon_element_class){
  let ic_element_class = "." + icon_element_class;

  $(ic_element_class).removeClass("fas fa-check-square");
  $(ic_element_class).removeClass("fas fa-square");
  $(ic_element_class).addClass("fas fa-check-square");
}

// opposite import between zero and one
function opposite_input_value(input_element_id){
  let ip_element_id = "#" + input_element_id;
  if($(ip_element_id).val() == "0"){
    $(ip_element_id).val("1");
  }
  else{
    $(ip_element_id).val("0");
  }
}

// change icon and input value to opposite
function change_checkbox_icon_and_input_value(input_element_id, icon_element_id){
  opposite_input_value(input_element_id);
  change_checkbox_icon_base_on_element_value(input_element_id, icon_element_id);
}

// movie detail configs step 1
function movie_detail_configs_make_step1(){
  $('#movie_detail_configs_modal_next').attr("onclick","movie_detail_configs_make_step2()");

  $('#movie_detail_configs_modal_title_step_1').show();
  $('#movie_detail_configs_modal_title_step_2').hide();
  $('#movie_detail_configs_modal_title_step_3').hide();
  $('#movie_detail_configs_modal_step_1').show();
  $('#movie_detail_configs_modal_step_2').hide();
  $('#movie_detail_configs_modal_step_3').hide();

  $('#movie_detail_configs_modal_next').show(); 
  $('#movie_detail_configs_modal_previous').hide();

  $('#movie_detail_configs_modal_footer').show();
  $('#movie_detail_configs_modal_footer_step_final').hide();
}

// movie detail configs step 2
function movie_detail_configs_make_step2(){
  $('#movie_detail_configs_modal_next').attr("onclick","movie_detail_configs_make_step3()");
  $('#movie_detail_configs_modal_previous').attr("onclick","movie_detail_configs_make_step1()");

  $('#movie_detail_configs_modal_title_step_1').hide();
  $('#movie_detail_configs_modal_title_step_2').show();
  $('#movie_detail_configs_modal_title_step_3').hide();
  $('#movie_detail_configs_modal_step_1').hide();
  $('#movie_detail_configs_modal_step_2').show();
  $('#movie_detail_configs_modal_step_3').hide();

  $('#movie_detail_configs_modal_next').show();
  $('#movie_detail_configs_modal_previous').show();
  
  $('#movie_detail_configs_modal_footer').show();
  $('#movie_detail_configs_modal_footer_step_final').hide();
}

// movie detail configs step 3
function movie_detail_configs_make_step3(){
  $('#movie_detail_configs_modal_previous').attr("onclick","movie_detail_configs_make_step2()");

  $('#movie_detail_configs_modal_title_step_1').hide();
  $('#movie_detail_configs_modal_title_step_2').hide();
  $('#movie_detail_configs_modal_title_step_3').show();
  $('#movie_detail_configs_modal_step_1').hide();
  $('#movie_detail_configs_modal_step_2').hide();
  $('#movie_detail_configs_modal_step_3').show();

  $('#movie_detail_configs_modal_next').hide();
  $('#movie_detail_configs_modal_previous').show();
  
  $('#movie_detail_configs_modal_footer').hide();
  $('#movie_detail_configs_modal_footer_step_final').show();
  
  allow_submit_button_if_form_complete('add_or_update_movie_detail_form', 'add_or_update_movie_detail_form_submit_btn');
}

// create pure movie name en
function create_pure_mv_name_en(mv_name){
  let cut_index = mv_name.indexOf('(', 0);
  let mv_name_edit = "";
  if(cut_index < 0){
    mv_name_edit = mv_name;
  }
  else{
    mv_name_edit = mv_name.substr(0, cut_index);
  }
  return mv_name_edit
}