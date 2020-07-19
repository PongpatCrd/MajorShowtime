// make time setting branches time modal step 1
function time_detail_configs_make_step_1(){
  $('#time_setting_configs_modal_next').attr("onclick","time_detail_configs_make_step_2()");

  $('#time_setting_configs_modal_title_step_1').show();
  $('#time_setting_configs_modal_title_step_2').hide();
  $('#time_setting_configs_modal_title_step_3').hide();
  $('#time_setting_configs_modal_step_1').show();
  $('#time_setting_configs_modal_step_2').hide();
  $('#time_setting_configs_modal_step_3').hide();

  $('#time_setting_configs_modal_next').show(); 
  $('#time_setting_configs_modal_previous').hide();

  $('#time_setting_configs_modal_footer').show();
  $('#time_setting_configs_modal_footer_step_final').hide();
}

// make time setting branches time modal step 2
function time_detail_configs_make_step_2(){
  $('#time_setting_configs_modal_previous').attr("onclick","time_detail_configs_make_step_1()");

  $('#time_setting_configs_modal_title_step_1').hide();
  $('#time_setting_configs_modal_title_step_2').show();
  $('#time_setting_configs_modal_step_1').hide();
  $('#time_setting_configs_modal_step_2').show();

  $('#time_setting_configs_modal_next').hide(); 
  $('#time_setting_configs_modal_previous').show();

  $('#time_setting_configs_modal_footer').hide();
  $('#time_setting_configs_modal_footer_step_final').show();
}
