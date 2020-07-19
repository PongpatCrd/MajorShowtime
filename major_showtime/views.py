from major_showtime.models import *
from major_showtime.functions import *
from datetime import *

from django.db import transaction
from django.http import JsonResponse
from django.template.loader import render_to_string
from django.shortcuts import render
from django.db.models import Max
from django.core.paginator import Paginator, EmptyPage

# Create your views here.
def home(request):
  branch_regions = BranchesRegionSetting.objects.values_list('branch_region', flat=True).distinct()
  max_n_screen = TblBranch.objects.using('ticket_sale').aggregate(Max('branch_notheatre'))['branch_notheatre__max']

  if len(request.GET) != 0:
    branch_region = request.GET.get('select_region', 'all')
    n_back_date = int(request.GET.get('select_back_date'))
    n_screen = request.GET.get('select_n_screen')

    if n_back_date == None:
      n_back_date = 14
    if n_screen.lower() in ['all', None]:
      n_screen_list = [i for i in range(1, max_n_screen+1)]
    else:
      n_screen_list = [int(n_screen)]

    admis_each_movie, total_admis_each_day = get_admis_dashboard_n_days(n_back_date, branch_region, n_screen_list)

    admis_each_movie_dataset     = gen_line_chart_formated_dataset(admis_each_movie)
    total_admis_each_day_dataset = gen_line_chart_formated_dataset(total_admis_each_day)
  else:
    admis_each_movie_dataset = {}
    total_admis_each_day_dataset = {}

  context = {
    'branch_regions'              : branch_regions,
    'max_n_screen'                : max_n_screen,
    'admis_each_movie_dataset'    : admis_each_movie_dataset,
    'total_admis_each_day_dataset': total_admis_each_day_dataset,
  }

  return render(request, 'home.html', context)

def movies(request):
  page = request.GET.get('page', 1)
  n_show_movies = request.GET.get('select_n_show_movies', 100)
  search_movie = request.GET.get('search_movie', '')

  tbl_mv_details = get_tbl_mv_details_with_search_key(search_movie)
  if n_show_movies != 'all':
    n_show_movies = int(n_show_movies)
    paginator = Paginator(tbl_mv_details[:n_show_movies], 50)
  else:
    paginator = Paginator(tbl_mv_details, 50)
  try:
    paginator_tbl_mv_details = paginator.page(page)
  except EmptyPage:
    paginator_tbl_mv_details = paginator.page(paginator.num_pages)

  langs = TblMvlanguage.objects.using('ticket_sale').values('mvlang_id', 'mvlang_ename')
  nations = TblMvnation.objects.using('ticket_sale').values('mvnation_id', 'mvnation_ename')
  genres = TblMvgenre.objects.using('ticket_sale').values('mvgenre_id', 'mvgenre_ename')
  distributors = TblDistributor.objects.using('ticket_sale').values('distributor_id', 'distributor_name').filter(distributor_status=True).order_by('distributor_name')
  mvformats = TblMvformat.objects.using('ticket_sale').values('format_strcode', 'format_strname').exclude(format_strcode='VS00000001')

  context = {
    'tbl_mv_details'      :paginator_tbl_mv_details,
    'lang_details'        :langs,
    'nation_details'      :nations,
    'genre_details'       :genres,
    'distributor_details' :distributors,
    'mvformats'           :mvformats
  }
  return render(request, 'movies.html', context)

def movie_status_configs(request):
  def input_validation():
    return True, "success"
  page = request.POST.get('page', 1)
  n_show_movies = int(request.POST.get('select_n_show_movies', 100))
  search_movie = request.POST.get('search_movie', '')
  
  mv_ids = request.POST.getlist('mv_id_movie_status_selection')
  status_movies = request.POST.getlist('status_movie_status_selection')

  success, msg = input_validation()

  if success:
    to_inactive_list = []
    to_active_list = []
    for i in range(len(mv_ids)):
      if status_movies[i] == "1":
        to_active_list.append(mv_ids[i])
      elif status_movies[i] == "0":
        to_inactive_list.append(mv_ids[i])
    update_tbl_mv_status(to_active_list, to_inactive_list)

  tbl_mv_details = get_tbl_mv_details_with_search_key(search_movie)

  paginator = Paginator(tbl_mv_details[:n_show_movies], 50)
  try:
    paginator_tbl_mv_details = paginator.page(page)
  except EmptyPage:
    paginator_tbl_mv_details = paginator.page(paginator.num_pages)

  movies_table_html = render_to_string('movies_table.html', {'tbl_mv_details': paginator_tbl_mv_details}, request=request)

  movies_multiple_status_selection_modal_html = render_to_string('movies_multiple_status_selection_modal.html', {'tbl_mv_details': paginator_tbl_mv_details},request=request)

  response = {
    'movies_table_html'                          : movies_table_html,
    'movies_multiple_status_selection_modal_html': movies_multiple_status_selection_modal_html,
    'status_msg'                                 : msg,
  }

  return JsonResponse(response)

# @transaction.atomic
def add_or_update_movie_detail(request):
  mv_id               = request.POST.get('mv_id', '')
  mv_name_en          = request.POST.get('mv_name_en', '')
  pure_mv_name_en     = request.POST.get('pure_mv_name_en', '')
  mv_short_name       = request.POST.get('mv_short_name', '')
  mv_name_th          = request.POST.get('mv_name_th', '')
  actor_name          = request.POST.get('actor_name', '')
  actress_name        = request.POST.get('actress_name', '')
  format_details      = request.POST.getlist('format_details', '')
  nation_id           = request.POST.get('nation_id', '')
  genre_id            = request.POST.get('genre_id', '')
  mv_desc             = request.POST.get('mv_desc', '')
  income_estimate     = request.POST.get('income_estimate', '')
  distributor_id      = request.POST.get('distributor_id', '')
  duration            = request.POST.get('duration', '')
  advertisement_time  = request.POST.get('advertisement_time', '')
  advertisement_time  = change_empty_to_given_value(income_estimate, 0)
  release_date        = request.POST.get('release_date', '')
  expire_date         = request.POST.get('expire_date', '')
  mv_status           = request.POST.get('mv_status', '')

  try:
    release_date = release_date.split('-')
    release_date = release_date[2] + release_date[1] + release_date[0]
  except: 
    release_date = ''
  try:
    expire_date = expire_date.split('-')
    expire_date = expire_date[2] + expire_date[1] + expire_date[0]
  except:
    expire_date = ''

  current_datetime = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
  msg = ''

  data_dict = {
    'mv_ename'      : mv_name_en,
    'mv_tname'      : mv_name_th,
    'mv_kname'      : pure_mv_name_en,
    'mv_sname'      : mv_short_name,
    'mv_actor'      : actor_name,
    'mv_actress'    : actress_name,
    'distributor_id': distributor_id,
    'mv_time'       : duration,
    'mv_adtime'     : advertisement_time,
    'mv_releasedate': release_date,
    'mv_expiredate' : expire_date,
    'mv_desc'       : mv_desc,
    'mv_status'     : mv_status,
    'lastupdate'    : current_datetime,
    'mvnation_id'   : nation_id,
    'mvgenre_id'    : genre_id
  }

  if mv_id:
    # update
    try:
      with transaction.atomic():
        mv_details = TblMv.objects.using('ticket_sale').filter(mv_id=mv_id).update(**data_dict)

        movie_estimated_income = MovieEstimatedIncome.objects.values().filter(mv_id=mv_id)
        if movie_estimated_income:
          movie_estimated_income.update(income_estimated=income_estimate)
        else:
          MovieEstimatedIncome.objects.create(mv_id=mv_id,income_estimated=income_estimate)
    except:
      msg = 'Error while update movie details.'
  else:
    # create
    try:
      with transaction.atomic():
        mv_id = gen_mv_id()
        data_dict['mv_id'] = mv_id
        mv_details = TblMv(**data_dict).save(using='ticket_sale')
        MovieEstimatedIncome.objects.create(mv_id=mv_id, income_estimated=income_estimate)
    except:
      msg = 'Error while add new movie.'
  
  if msg == '':
    try:
      tbl_mvformat_detail_list = []
      with transaction.atomic():
        TblMvformatdetail.objects.using('ticket_sale').filter(mv_id=mv_id).delete()
        for format_detail in format_details:
          tbl_mvformat_detail_list.append(TblMvformatdetail(mv_id=mv_id, format_strcode=format_detail, createdate=current_datetime))
        TblMvformatdetail.objects.using('ticket_sale').bulk_create(tbl_mvformat_detail_list)
    except:
      msg = 'Error while create format detail'

  # movies_table_html
  tbl_mv_details = get_tbl_mv_details_with_search_key('')
  paginator = Paginator(tbl_mv_details[:100], 50)
  try:
    paginator_tbl_mv_details = paginator.page(1)
  except EmptyPage:
    paginator_tbl_mv_details = paginator.page(paginator.num_pages)

  context = {
    'tbl_mv_details': paginator_tbl_mv_details
  }
  movies_table_html = render_to_string('movies_table.html', context, request=request)

  # movies_multiple_status_selection_modal_html
  movies_multiple_status_selection_modal_html = render_to_string('movies_multiple_status_selection_modal.html', context, request=request)


  msg = ""
  response = {
    'movies_table_html'                          : movies_table_html,
    'movies_multiple_status_selection_modal_html': movies_multiple_status_selection_modal_html,
    'status_msg'                                 : msg
  }
  
  return JsonResponse(response)

def create_movie_detail_edit_modal(request):
  mv_id = request.GET.get('mv_id')
  movie_detail = TblMv.objects.using('ticket_sale').values('mv_id', 'mv_ename', 'mv_kname', 'mv_sname', 'mv_tname', 'mv_actor', 'mv_actress', 'distributor_id', 'mv_time', 'mv_adtime', 'mv_releasedate', 'mv_expiredate', 'mv_desc', 'mv_status', 'mvnation_id', 'mvgenre_id').filter(mv_id=mv_id)[0]
  format_details = list(TblMvformatdetail.objects.using('ticket_sale').values_list('format_strcode', flat=True).filter(mv_id=mv_id).distinct())
  movie_estimated_income = MovieEstimatedIncome.objects.values_list('income_estimated', flat=True).filter(mv_id=mv_id)

  if movie_estimated_income:
    movie_estimated_income = movie_estimated_income[0]
  else:
    movie_estimated_income = 0
  if movie_detail['mv_releasedate']:
    release_date = date(int(movie_detail['mv_releasedate'][:4]), int(movie_detail['mv_releasedate'][4:6]), int(movie_detail['mv_releasedate'][6:])).strftime('%d-%m-%Y')
  else:
    release_date = ''

  if movie_detail['mv_expiredate']:
    expire_date = date(int(movie_detail['mv_expiredate'][:4]), int(movie_detail['mv_expiredate'][4:6]), int(movie_detail['mv_expiredate'][6:])).strftime('%d-%m-%Y')
  else:
    expire_date = ''
  
  context = {
    'mv_id'             : movie_detail['mv_id'],
    'mv_name_en'        : movie_detail['mv_ename'],
    'pure_mv_name_en'   : movie_detail['mv_kname'],
    'mv_short_name'     : movie_detail['mv_sname'],
    'mv_name_th'        : movie_detail['mv_tname'],
    'actor_name'        : movie_detail['mv_actor'],
    'actress_name'      : movie_detail['mv_actress'],
    'format_details'    : format_details,
    'nation_id'         : movie_detail['mvnation_id'],
    'genre_id'          : movie_detail['mvgenre_id'],
    'mv_desc'           : movie_detail['mv_desc'],
    'mv_status'         : movie_detail['mv_status'],
    'income_estimate'   : movie_estimated_income,
    'distributor_id'    : movie_detail['distributor_id'],
    'duration'          : movie_detail['mv_time'],
    'advertisement_time': movie_detail['mv_adtime'],
    'release_date'      : release_date,
    'expire_date'       : expire_date,
  }

  movies_movie_detail_edit_modal_html = render_to_string('movies_movie_detail_edit_modal.html', {'movie_detail': context}, request=request)

  msg = ''

  response = {
    'movies_movie_detail_edit_modal_html': movies_movie_detail_edit_modal_html,
    'status_msg': msg,
  }

  return JsonResponse(response)

def time_setting(request):
  page = request.GET.get('page', 1)
  select_region = request.GET.get('select_region', 'all')
  search_time_setting = request.GET.get('search_time_setting', '')

  tbl_branch_details = get_tbl_branch_details(select_region)
  branches_nickname_list = extract_list_from_dict(tbl_branch_details, 'branch_nickname')
  branches_time_setting_map = get_branches_time_setting_map(branches_nickname_list)
  branches_best_time_map = get_branches_best_time_map(branches_nickname_list)
  
  formatted_datas = make_formatted_time_setting_data_dict(tbl_branch_details, branches_time_setting_map, branches_best_time_map, search_time_setting)
  
  paginator = Paginator(formatted_datas, 50)
  try:
    paginator_time_setting_dataset = paginator.page(page)
  except EmptyPage:
    paginator_time_setting_dataset = paginator.page(paginator.num_pages)

  branch_regions = BranchesRegionSetting.objects.values_list('branch_region', flat=True).distinct()
  context = {
    'branch_regions'      : branch_regions,
    'time_setting_dataset': paginator_time_setting_dataset
  }
  return render(request, 'time_setting.html', context)

@transaction.atomic
def update_branch_times(request):
  page = request.POST.get('page', 1)
  select_region = request.POST.get('select_region', '')
  search_time_setting = request.POST.get('search_time_setting', '')

  branch_nickname = request.POST.get('branch_nickname', '')
  first_showtime = request.POST.get('first_showtime', '')
  last_showtime = request.POST.get('last_showtime', '')
  advertisement_time = request.POST.get('advertisement_time', '')
  clean_up_time = request.POST.get('clean_up_time', '')
  break_time = request.POST.get('break_time', '')
  best_time_details = list(set(request.POST.getlist('best_time_details', [])))
  best_time_details.sort()
  
  branches_time_setting_data = {
    'branch_nickname'   : branch_nickname,
    'first_showtime'    : first_showtime,
    'last_showtime'     : last_showtime,
    'advertisement_time': advertisement_time,
    'clean_up_time'     : clean_up_time,
    'break_time'        : break_time,
    'is_active'         : True,
    'updated_at'        : datetime.now()
  }

  branches_time_setting = BranchesTimeSetting.objects.values().filter(branch_nickname=branch_nickname, is_active=True)
  if branches_time_setting:
    branches_time_setting.update(**branches_time_setting_data)
  else:
    BranchesTimeSetting(**branches_time_setting_data).save()

  branches_best_time_details = BranchesBestTimeDetail.objects.filter(branch_nickname=branch_nickname, is_active=True)
  old_best_time_details = list(branches_best_time_details.values_list('best_time', flat=True))
  old_keep_best_time_details = set(best_time_details).intersection(old_best_time_details)
  new_best_time_details = set(best_time_details).difference(old_keep_best_time_details)
  branches_best_time_details = branches_best_time_details.exclude(best_time__in=old_keep_best_time_details)
  
  if branches_best_time_details:
    branches_best_time_details.delete()

  if new_best_time_details:
    new_branches_best_time_details = []
    for best_time in new_best_time_details:
      new_branches_best_time_details.append(
        BranchesBestTimeDetail(branch_nickname=branch_nickname, best_time=best_time, is_active=True)
      )
    if new_branches_best_time_details:
      BranchesBestTimeDetail.objects.bulk_create(new_branches_best_time_details)
  
  tbl_branch_details = get_tbl_branch_details(select_region)
  branches_nickname_list = extract_list_from_dict(tbl_branch_details, 'branch_nickname')
  branches_time_setting_map = get_branches_time_setting_map(branches_nickname_list)
  branches_best_time_map = get_branches_best_time_map(branches_nickname_list)
  time_setting_formatted_dataset_list = make_formatted_time_setting_data_dict(tbl_branch_details, branches_time_setting_map, branches_best_time_map, search_time_setting)

  paginator = Paginator(time_setting_formatted_dataset_list, 50)
  try:
    paginator_time_setting_dataset = paginator.page(page)
  except EmptyPage:
    paginator_time_setting_dataset = paginator.page(paginator.num_pages)
  except:
    paginator_time_setting_dataset = paginator.page(1)

  context = {
    'time_setting_dataset': paginator_time_setting_dataset
  }

  time_setting_branches_time_table_html = render_to_string('time_setting_branches_time_table.html', context, request=request)
  msg = ''

  response = {
    'time_setting_branches_time_table_html': time_setting_branches_time_table_html,
    'status_msg': msg
  }

  return JsonResponse(response)

def showtimes(request):
  # showtime_date: YYYYMMDD
  showtime_datasets = {}
  movie_format_map = {}

  select_region = request.GET.get('select_region', 'all')
  showtime_date = request.GET.get('showtime_date', '')
  n_screen = request.GET.get('select_n_screen', 1)
  search_showtime = request.GET.get('search_showtime', '')
  page = request.GET.get('page', 1)

  max_n_screen = TblBranch.objects.using('ticket_sale').aggregate(Max('branch_notheatre'))['branch_notheatre__max']
  branch_regions = BranchesRegionSetting.objects.values_list('branch_region', flat=True).distinct()

  if showtime_date:
    if showtime_date != '':
      program_date = showtime_date.split('-')
      program_date = program_date[-1] + program_date[-2] + program_date[-3]

      showtime_datasets = make_formatted_showtime_branches_box_data_dict(select_region, n_screen, program_date, search_showtime)

    paginator = Paginator(showtime_datasets, 10)
    try:
      paginator_showtime_datasets = paginator.page(page)
    except EmptyPage:
      paginator_showtime_datasets = paginator.page(paginator.num_pages)
    except:
      paginator_showtime_datasets = paginator.page(1)

    select_n_show_movies = request.GET.get('select_n_show_movies', 300)
    if select_n_show_movies == 'all':
      tbl_mv_details = TblMv.objects.using('ticket_sale').values('mv_id', 'mv_ename', 'mv_kname', 'mv_time').order_by('-mv_releasedate')
    else:
      tbl_mv_details = TblMv.objects.using('ticket_sale').values('mv_id', 'mv_ename', 'mv_kname', 'mv_time').order_by('-mv_releasedate')[:int(select_n_show_movies)]

    tbl_mvlanguage_details = TblMvlanguage.objects.using('ticket_sale').values('mvlang_id', 'mvlang_ename')
    movie_format_map = get_movie_format_map(list(tbl_mv_details.values_list('mv_id', flat=True)))
    
    context = {
      'paginator_showtime_datasets' : paginator_showtime_datasets,
      'mv_details'                  : tbl_mv_details,
      'branch_regions'              : branch_regions,
      'lang_details'                : tbl_mvlanguage_details,
      'movie_format_map'            : movie_format_map,
      'max_n_screen'                : max_n_screen,
      'n_screen'                    : n_screen,
      'all_showtime_datasets'       : showtime_datasets
    }
  else:
    context = {'max_n_screen': max_n_screen, 'branch_regions': branch_regions, 'movie_format_map': movie_format_map}
  
  return render(request, 'showtimes.html', context)

def update_showtime_screen_details(request):
  msg = ''
  showtime_branch_selection_modal_html = ''
  showtime_branch_box_card_html = ''

  showtimes = request.POST.getlist('showtime[]', [])
  mv_ids = request.POST.getlist('mv_id[]', [])
  mv_formats = request.POST.getlist('mv_format[]', [])
  langs = request.POST.getlist('lang[]', [])

  screens = request.POST.getlist('screen[]', [])
  # 2 below use together ex choose_status_branch_code_details[0] will use choose_status[0] as status
  choose_status_branch_code_details = request.POST.getlist('choose_status_branch_code_detail[]', [])
  choose_status = request.POST.getlist('choose_status[]', [])
  
  showtime_date = request.POST.get('showtime_date', '')
  db_format_program_date = ''
  if showtime_date:
    temp = showtime_date.split('-')
    db_format_program_date = temp[-1] + temp[-2] + temp[-3]

    branch_nickname_list = []
    for branch_detail_idx in range(len(choose_status_branch_code_details)):
      if choose_status[branch_detail_idx] == '1':
        branch_nickname_list.append(choose_status_branch_code_details[branch_detail_idx])
    
    delete_current_showtime(branch_nickname_list, db_format_program_date)

    client_ip = get_client_ip(request)
    current_datetime = datetime.today().strftime('%Y-%m-%d %H:%M:%S.%f')[:-3]
    new_mvprogram_objects = []
    for branch_nickname in branch_nickname_list:
      for detail_idx in range(len(showtimes)):
          if screens[detail_idx] and showtimes[detail_idx] and mv_ids[detail_idx] and langs[detail_idx] and mv_formats[detail_idx]:
            temp = TblMvprogram(
              branch_id      = branch_nickname,
              theatre        = screens[detail_idx],
              program_date   = db_format_program_date,
              program_time   = showtimes[detail_idx],
              mv_id          = mv_ids[detail_idx],
              mvlang_id      = langs[detail_idx],
              lastupdate     = current_datetime,
              ipupdate       = client_ip,
              format_strcode = mv_formats[detail_idx]
            )
            new_mvprogram_objects.append(temp)
    if new_mvprogram_objects:
      TblMvprogram.objects.using('ticket_sale').bulk_create(new_mvprogram_objects)
  else:
    pass
  search_showtime = request.POST.get('search_showtime', '')
  select_n_screen = request.POST.get('select_n_screen', 1)
  select_region = request.POST.get('select_region', 'all')
  try:
    page = int(request.POST.get('page', 1))
  except:
    page = 1
  showtime_datasets = make_formatted_showtime_branches_box_data_dict(select_region, select_n_screen, db_format_program_date, search_showtime)

  paginator = Paginator(showtime_datasets, 10)
  try:
    paginator_showtime_datasets = paginator.page(page)
  except EmptyPage:
    paginator_showtime_datasets = paginator.page(paginator.num_pages)
  except:
    paginator_showtime_datasets = paginator.page(1)
  
  showtime_branch_selection_modal_html = render_to_string('showtime_branch_selection_modal.html', {'all_showtime_datasets': showtime_datasets})
  showtime_branch_box_card_html = render_to_string('showtime_branch_box_card.html', {'showtime_datasets': paginator_showtime_datasets}, request=request)

  response = {
    'showtime_branch_selection_modal_html': showtime_branch_selection_modal_html,
    'showtime_branch_box_card_html'      : showtime_branch_box_card_html,
    'status_msg'                          : msg
  }
  return JsonResponse(response)

def region_setting(request):
  page = request.GET.get('page', 1)
  branch_details = get_region_setting_details()

  search_key = request.GET.get('search_region_setting', '')
  if search_key:
    branch_details = search_with_key(branch_details, search_key)
  paginator = Paginator(branch_details, 50)
  try:
    paginator_branch_details = paginator.page(page)
  except EmptyPage:
    paginator_branch_details = paginator.page(paginator.num_pages)

  context = {
    'paginator_branch_details': paginator_branch_details
  }
  return render(request, 'branch_region_setting.html', context)

def create_or_update_region(request):
  branch_nickname = request.POST.get('branch_nickname', '')
  branch_codevista = request.POST.get('branch_codevista', '')
  select_region = request.POST.get('region', '')
  msg = "Error while update region, Please refresh whole page and try again."

  if branch_codevista and branch_codevista and (select_region != "None" and select_region):
    branches_region_setting = BranchesRegionSetting.objects.all().filter(branch_code_vista=branch_codevista)
    if branches_region_setting:
      branches_region_setting.update(branch_region=select_region)
    else:
      BranchesRegionSetting.objects.create(
        branch_nickname   = branch_nickname,
        branch_code_vista = branch_codevista,
        branch_region     = select_region
      )
    msg = "success"

  return JsonResponse({'msg': msg})