import random
import os
import re
import math

from datetime import datetime, timedelta
from django.db.models import Q, Max
from major_showtime.models import *

def base_mv_name(mv_name):
  return mv_name[:mv_name.find('(')]

def get_tbl_branch_details(branch_region='all', n_screen='all'):
  '''
  branch_region: str
  n_screen: str ex.(1, 2, 3, all)
  '''
  tbl_branch_branch_servernames = TblBranch.objects.using('ticket_sale').values('branch_servername').filter(branch_status=True, branch_notheatre__gt=0).annotate(max_branch_notheatre=Max('branch_notheatre'))
  tbl_branch_branch_servernames_map = { detail['branch_servername'].lower(): detail['max_branch_notheatre'] for detail in tbl_branch_branch_servernames }

  tbl_branch_details = TblBranch.objects.using('ticket_sale').values(
      'branch_servername',
      'branch_nickname',
      'branch_notheatre'
    ).filter(branch_status=True, branch_notheatre__gt=0)

  branch_nickname_without_imax_in_same_complex = []
  for detail in tbl_branch_details:
    if tbl_branch_branch_servernames_map[detail['branch_servername'].lower()] == detail['branch_notheatre']:
      branch_nickname_without_imax_in_same_complex.append(detail['branch_nickname'])

  if branch_region.lower() != 'all':
    branch_region_list = [branch_region]
    branch_nickname_from_region = list(BranchesRegionSetting.objects.values_list('branch_nickname', flat=True).filter(branch_region__in=branch_region_list))
    branch_nickname_without_imax_in_same_complex = list(set(branch_nickname_without_imax_in_same_complex) & set(branch_nickname_from_region))

  tbl_branch_details = TblBranch.objects.using('ticket_sale').values(
    'branchcodevista',
    'branch_fullname',
    'branch_thainame',
    'branch_nickname',
    'branch_notheatre'
  ).filter(branch_nickname__in=branch_nickname_without_imax_in_same_complex).order_by('branch_notheatre', 'branch_fullname')
  
  branch_region_map = {detail['branch_nickname']: detail['branch_region'] for detail in BranchesRegionSetting.objects.values('branch_nickname', 'branch_region')}
  for tbl_branch_detail in tbl_branch_details:
    try:
      tbl_branch_detail['branch_region'] = branch_region_map[tbl_branch_detail['branch_nickname']]
    except:
      tbl_branch_detail['branch_region'] = None
  
  if n_screen != 'all':
    temp = []
    for tbl_branch_detail in tbl_branch_details:
      if str(tbl_branch_detail['branch_notheatre']) == str(n_screen):
        temp.append(tbl_branch_detail)
    tbl_branch_details = temp
  return tbl_branch_details

def get_admis_dashboard_n_days(n_back_date, region, n_screen_list):
  temp_minus_date = timedelta(days=1)
  current_date = datetime.today().date()
  
  back_date_list = []
  for num in range(n_back_date):
    current_date -= temp_minus_date
    back_date_list.append(current_date.strftime('%Y%m%d'))

  tbl_branch_details = get_tbl_branch_details(region)

  branch_nicknames = [detail['branch_nickname'] for detail in tbl_branch_details]

  branch_code2_list = TblBranch.objects.using('ticket_sale').values_list('branch_id', flat=True).filter(
    branch_status=1,
    branch_notheatre__in=n_screen_list,
    branch_nickname__in=branch_nicknames
  )

  tbl_sum_movie_seat_new_details = TblSummovieseatnew.objects.using('ticket_sale').values(
    'datesum',
    'mvname',
    'admis'
  ).filter(datesum__in=back_date_list, branchid__in=branch_code2_list).order_by('datesum', 'mvname')

  admis_each_movies = {}
  total_admis_each_days = {}
  for detail in tbl_sum_movie_seat_new_details:
    # total_admis_each_days
    try:
      total_admis_each_days[detail['datesum']]['admissions'] += int(detail['admis'])
    except:
      total_admis_each_days[detail['datesum']] = {
        'admissions': int(detail['admis']),
      }
      admis_each_movies[detail['datesum']] = {}

    # admis_each_movies
    mv_name = base_mv_name(detail['mvname'])
    try:
      admis_each_movies[detail['datesum']][mv_name] += int(detail['admis'])
    except:
      admis_each_movies[detail['datesum']][mv_name] = int(detail['admis'])

  return admis_each_movies, total_admis_each_days

def rendom_color_code():
  r = lambda: random.randint(0,255)
  return '#%02X%02X%02X' % (r(),r(),r())

def gen_line_chart_formated_dataset(dataset_dict):
  # dataset_dict format
  # {
  #   x_label: {
  #     label: data,
  #     label: data,
  #     ...
  #   }
  # }
  # example datasetformat use in chart.js
  #   {
  #   datasets: [{
  #       label: 'First dataset',
  #       data: [0, 20, 40, 50]
  #   }],
  #   labels: ['January', 'February', 'March', 'April']
  # },...

  dataset_label = []
  for _, label_name in dataset_dict.items():
    temp = list(label_name.keys())
    dataset_label += temp
  dataset_label = list(set(dataset_label))

  each_datasets = {}
  already_use_color = []
  for label_name in dataset_label:
    while True:
      color = rendom_color_code()
      if color not in already_use_color:
        already_use_color.append(color)
        each_datasets[label_name] = {
          'label'          : label_name,
          'data'           : [],
          'backgroundColor': already_use_color[-1],
          'borderColor'    : already_use_color[-1],
          'fill'           : 'false'
        }
        break

  labels = []
  for datesum, dataset_details in dataset_dict.items():
    labels.append(
      "{}-{}-{}".format(datesum[:4], datesum[4:6], datesum[6:])
    )

    # this will append 0 to that day if it doesn't have admis data
    list_label_names_this_day = dataset_details.keys()
    for label_name in each_datasets.keys():
      if label_name in list_label_names_this_day:
        each_datasets[label_name]['data'].append(dataset_details[label_name])
      else:
        each_datasets[label_name]['data'].append(0)

  ans_dataset = {'datasets': []}
  for each_movie_each_day in each_datasets.values():
    ans_dataset['datasets'].append(each_movie_each_day)
  
  ans_dataset['labels'] = labels
  return ans_dataset

def get_tbl_mv_details_with_search_key(search_movie_key):
  tbl_mv_details = TblMv.objects.using('ticket_sale').values('mv_id', 'mv_ename', 'mv_sname', 'mv_time', 'mv_releasedate', 'mv_status')
  
  if search_movie_key != '':
    tbl_mv_details = tbl_mv_details.filter(
      Q(mv_ename__icontains=search_movie_key) |
      Q(mv_sname__icontains=search_movie_key) |
      Q(mv_releasedate__icontains=search_movie_key)
    )
  
  tbl_mv_details = tbl_mv_details.order_by('-mv_releasedate')
  return tbl_mv_details

def update_tbl_mv_status(to_active_list, to_inactive_list):
  to_active_tbl_mv_details = TblMv.objects.using('ticket_sale').filter(mv_id__in=to_active_list).update(mv_status=True)
  to_inactive_tbl_mv_details = TblMv.objects.using('ticket_sale').filter(mv_id__in=to_inactive_list).update(mv_status=False)
  return True

def change_empty_to_given_value(input_value, given_value):
  if input_value != '':
    return given_value
  else:
    return None

def gen_mv_id():
  return int(list(TblMv.objects.using('ticket_sale').aggregate(Max('mv_id')).values())[0]) + 1

def extract_list_from_dict(data_dict, column_name):
  list_extract = []
  for detail in data_dict:
    list_extract.append(detail[column_name])
  return list_extract

def get_branches_time_setting_map(branch_nickname_list):
  branches_time_setting_details = BranchesTimeSetting.objects.values().filter(is_active=True, branch_nickname__in=branch_nickname_list)
  
  branches_time_setting_map = {}
  for branches_time_setting_detail in branches_time_setting_details:
    branch_nickname = branches_time_setting_detail['branch_nickname']
    branches_time_setting_map[branch_nickname] = branches_time_setting_detail
  
  return branches_time_setting_map

def get_branches_best_time_map(branch_nickname_list):
  # format of output # {'branch_nickname': [], 'branch_nickname': [], ...}
  branches_best_time_details = BranchesBestTimeDetail.objects.values().filter(is_active=True, branch_nickname__in=branch_nickname_list).order_by('branch_nickname', 'best_time')

  branches_best_time_map = {}
  for branches_best_time_detail in branches_best_time_details:
    try:
      branches_best_time_map[branches_best_time_detail['branch_nickname']].append(branches_best_time_detail['best_time'])
    except:
      branches_best_time_map[branches_best_time_detail['branch_nickname']] = [branches_best_time_detail['best_time']]
  return branches_best_time_map

# cal similarity of data_list and given search_key  (data_list of one record)
def cal_similarity_with_search_key(data_list, search_key):
  one_line_data = re.sub("[\[\]\,\ ]", "", str(data_list)).lower()
  default_len = len(one_line_data)

  for word in search_key.split(' '):
    one_line_data = one_line_data.replace(word.lower(), '')
  new_len = len(one_line_data)

  similarity_rate = 1.0 - (new_len/default_len)
  return similarity_rate
  
def search_with_key(list_of_datas, search_key):
  search_datas = []
  similarity_rate_list = []
  for data in list_of_datas:
    cal_similarity_rate = cal_similarity_with_search_key(data, search_key)
    idx = 0
    if cal_similarity_rate > 0:
      for i in range(len(similarity_rate_list)):
        if cal_similarity_rate >= similarity_rate_list[i]:
          idx = i
      similarity_rate_list.insert(idx, cal_similarity_rate)
      search_datas.insert(idx, data)
  
  search_datas.reverse()
  return search_datas

def make_formatted_time_setting_data_dict(tbl_branch_details, branches_time_setting_map, branches_best_time_map, search_key=''):
  # output format
  # [
  #   {
  #     'branch_nickname'    : str or '' for empty,
  #     'branch_fullname'    : str or '' for empty,
  #     'branch_region'      : str or '' for empty,
  #     'branch_notheatre'   : int or '' for empty,
  #     'first_showtime'     : str or '' for empty,
  #     'last_showtime'      : str or '' for empty,
  #     'advertisement_time' : int or '' for empty,
  #     'clean_up_time'      : int or '' for empty,
  #     'break_time'         : int or '' for empty,
  #     'best_time':         : arr of str
  #   },...
  # ]
  # order of data by ['branch_nickname', 'branch_notheatre'] default from tbl_branch_details

  for tbl_branch_detail in tbl_branch_details:
    temp_branch_time = branches_time_setting_map.get(tbl_branch_detail['branch_nickname'], {})

    tbl_branch_detail['first_showtime'] = temp_branch_time.get('first_showtime', '')
    tbl_branch_detail['last_showtime'] = temp_branch_time.get('last_showtime', '')
    tbl_branch_detail['advertisement_time'] = temp_branch_time.get('advertisement_time', '')
    tbl_branch_detail['clean_up_time'] = temp_branch_time.get('clean_up_time', '')
    tbl_branch_detail['break_time'] = temp_branch_time.get('break_time', '')
    tbl_branch_detail['best_time'] = branches_best_time_map.get(tbl_branch_detail['branch_nickname'], [])

  if search_key:
    formatted_datas = search_with_key(tbl_branch_details, search_key)
  else:
    formatted_datas = tbl_branch_details
  return formatted_datas

def get_showtime_detail_map(branch_nickname_list, program_date):
  # output format
  # {
  #   '{{branch_nickname}}': arr of tbl_mvprogram_details_object
  # }
  showtime_detail_map = {}
  tbl_mvprogram_details = TblMvprogram.objects.using('ticket_sale').values('branch_id', 'theatre','program_time', 'mv_id', 'mvlang_id', 'format_strcode').filter(branch_id__in=branch_nickname_list, program_date=program_date)
  
  for detail in tbl_mvprogram_details:
    try:
      showtime_detail_map[detail['branch_id']].append(detail)
    except:
      showtime_detail_map[detail['branch_id']] = [detail]
  return showtime_detail_map

def get_theatre_detail_map(branch_nickname_list):
  # output format
  # {
  #   '{{branch_nickname}}': [
  #     {
  #       'screen_number': int,
  #       'screen_name'  : str
  #     }
  #   ]
  # }
  branches_screen_details = BranchesScreenDetail.objects.values().filter(branch_nickname__in=branch_nickname_list)
  
  theatre_detail_map = {}
  for branch_nickname in branch_nickname_list:
    theatre_detail_map[branch_nickname] = {}

  for detail in branches_screen_details:
    screen_name = detail['screen_name'].strip()
    theatre_detail_map[detail['branch_nickname']][detail['screen_number']] = screen_name + " [{}]".format(str(detail['n_seat']))
    
  return theatre_detail_map

def make_formatted_showtime_branches_box_data_dict(branch_region, n_screen, program_date, search_key=''):
  # output format
  # [
  #   {
  #     'branch_nickname'       : str or '' for empty,
  #     'branch_fullname'       : str or '' for empty,
  #     'branch_region'         : str or '' for empty,
  #     'branch_notheatre'      : int or '' for empty,
  #     'branch_theatre_details': { {{screen_number}}: {{screen_name}} },...
  #     'showtime_details'      : [{
  #                                 'mv_id'         : str, 
  #                                 'showtime'      : str,
  #                                 'mv_lang_id'    : str,
  #                                 'theatre'       : str,
  #                                 'format_strcode': str
  #                               },...],
  #     'n_theatre_use'           : int
  #   },...
  # ]
  showtime_datasets = []

  tbl_branch_details = get_tbl_branch_details(branch_region, n_screen)

  branch_nickname_list = [tbl_branch_detail['branch_nickname'] for tbl_branch_detail in tbl_branch_details]

  showtime_detail_map = get_showtime_detail_map(branch_nickname_list, program_date)
  theatre_detail_map = get_theatre_detail_map(branch_nickname_list)

  for branch_detail in tbl_branch_details:
    temp = {
      'branch_nickname'       : branch_detail['branch_nickname'],
      'branch_fullname'       : branch_detail['branch_fullname'],
      'branch_region'         : branch_detail['branch_region'],
      'branch_notheatre'      : branch_detail['branch_notheatre'],
      'branch_theatre_details': theatre_detail_map[branch_detail['branch_nickname']],
      'showtime_details'      : [],
      'n_theatre_use'         : 0
    }
    
    check_each_theatre = []
    try:
      for showtime_detail in showtime_detail_map[branch_detail['branch_nickname']]:
        temp['showtime_details'].append(
          {
            'mv_id'         : showtime_detail['mv_id'],
            'showtime'      : showtime_detail['program_time'],
            'mv_lang_id'    : showtime_detail['mvlang_id'],
            'theatre'       : showtime_detail['theatre'],
            'format_strcode': showtime_detail['format_strcode']
          }
        )
        check_each_theatre.append(showtime_detail['theatre'])
    except:
      pass

    temp['n_theatre_use'] = len(list(set(check_each_theatre)))
    word_check = str(temp['branch_nickname']) + str(temp['branch_fullname']) + str(temp['branch_region']) + "{}/{}".format(temp['n_theatre_use'], branch_detail['branch_notheatre'])
    similarity_rate = cal_similarity_with_search_key(word_check, search_key)

    if not search_key or similarity_rate > 0:
      showtime_datasets.append(temp)
  return showtime_datasets

def get_movie_format_map(mv_id_list, batch_size=1000):
  tbl_mvformat_details = TblMvformat.objects.using('ticket_sale').values('format_strcode', 'format_strname', 'format_strshortname').filter(format_strstatus='A')
  tbl_mvformat_details = { detail['format_strcode']: detail for detail in tbl_mvformat_details }
  
  tbl_mvformat_detail_details = []
  for i in range(math.ceil(len(mv_id_list)/batch_size)):
    tbl_mvformat_detail_details += list(TblMvformatdetail.objects.using('ticket_sale').values('mv_id', 'format_strcode').filter(mv_id__in=mv_id_list[i*batch_size:(batch_size*i)+batch_size]))
  
  movie_format_map = {}
  for tbl_mvformat_detail_detail in tbl_mvformat_detail_details:
    temp = {
      'format_strcode'     : tbl_mvformat_detail_detail['format_strcode'],
      'format_strshortname': tbl_mvformat_details[tbl_mvformat_detail_detail['format_strcode']]['format_strshortname']
    }
    try:
      if temp not in movie_format_map[tbl_mvformat_detail_detail['mv_id']]:
        movie_format_map[tbl_mvformat_detail_detail['mv_id']].append(temp)
    except:
      movie_format_map[tbl_mvformat_detail_detail['mv_id']] = [temp]

  some_mv_not_have_format_details = set(mv_id_list).difference(list(movie_format_map.keys()))
  temp_for_default_mv_format = {'format_strcode':'0000000004', 'format_strshortname': 'D' }
  for mv_id in some_mv_not_have_format_details:
    movie_format_map[mv_id] = [temp_for_default_mv_format]

  return movie_format_map

def get_client_ip(request):
  x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
  if x_forwarded_for:
    ip = x_forwarded_for.split(',')[0]
  else:
    ip = request.META.get('REMOTE_ADDR')
  return ip

def delete_current_showtime(branch_nickname_list, showtime_date):
  TblMvprogram.objects.using('ticket_sale').filter(branch_id__in=branch_nickname_list, program_date=showtime_date).delete()
  return

def get_branch_screen_name_map():
  branches_screen_details = BranchesScreenDetail.objects.values()
  
  branches_screen_name_map = {}
  for detail in branches_screen_details:
    temp = {
      'screen_number': detail['screen_number'],
      'screen_name'  : detail['screen_name']
    }
    try:
      branches_screen_name_map[detail['branch_nickname']].append(temp)
    except:
      branches_screen_name_map[detail['branch_nickname']] = [temp]
    
  return branches_screen_name_map
  
def get_region_setting_details():
  tbl_branch_details = get_tbl_branch_details()

  branches_region_settings = BranchesRegionSetting.objects.values()
  branches_region_settings = {detail['branch_nickname']: detail['branch_region'] for detail in branches_region_settings}

  formatted_data = []
  for detail in tbl_branch_details:
    try:
      detail['region'] = branches_region_settings[detail['branch_nickname']]
    except:
      detail['region'] = None
  return tbl_branch_details
  