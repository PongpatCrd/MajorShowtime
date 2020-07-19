import math
from pull_data_helper import *
from MajorShowtime import settings

import os, django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'MajorShowtime.settings')
django.setup()

from major_showtime.models import *

def main():
  branch_server_ip_map = get_all_branch_server_ip()
  pull_data_helper = PullDataHelper(uid='xxxx', pwd='xxxx', db_name='xxxx')

  column_name_list = ['[ScreenL_intId]', '[Screen_bytNum]', '[Screen_intSeats]']
  table_name = "[dbo].[tblScreen_Layout]"

  branch_screen_seat_map = {}
  branch_nickname_failed = []
  for branch_nickname, branch_server in branch_server_ip_map.items():
    try:
      db_con_branch = pull_data_helper.generate_dbconn(branch_server)
      sql = pull_data_helper.generate_sql_select(column_name_list=column_name_list, table_name=table_name)

      cursor = db_con_branch.execute(sql)
      for detail in cursor.fetchall():
        try:
          branch_screen_seat_map[branch_nickname][detail.Screen_bytNum] = detail.Screen_intSeats
        except:
          branch_screen_seat_map[branch_nickname] = {detail.Screen_bytNum: detail.Screen_intSeats}
      print(branch_nickname, "==> Success")
    except:
      branch_nickname_failed.append(branch_nickname)
      print(branch_nickname, "==> Failed")
  
  branches_screen_details = BranchesScreenDetail.objects.all()

  for branches_screen_detail in branches_screen_details:
    try:
      branches_screen_detail.n_seat = branch_screen_seat_map[branches_screen_detail.branch_nickname][branches_screen_detail.screen_number]
      branches_screen_detail.save()
    except: 
      pass
