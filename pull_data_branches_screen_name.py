import math
from pull_data_helper import *

def main():
  branch_server_ip_map = get_all_branch_server_ip()
  pull_data_helper = PullDataHelper(uid='xxxx', pwd='xxxx', db_name='xxxx')

  column_name_list = ['[Screen_bytNum]', '[Screen_strName]']
  table_name = "[dbo].[tblCinema_Screen]"
  
  values_set_list = []
  branch_nickname_failed = []
  for branch_nickname, branch_server in branch_server_ip_map.items():
    try:
      db_con_branch = pull_data_helper.generate_dbconn(branch_server)
      sql = pull_data_helper.generate_sql_select(column_name_list=column_name_list, table_name=table_name)

      cursor = db_con_branch.execute(sql)
      for detail in cursor.fetchall():
        temp = "('{}', ".format(branch_nickname) + str(detail)[1:]
        values_set_list.append(temp)
      print(branch_nickname, "==> Success")
    except:
      branch_nickname_failed.append(branch_nickname)
      print(branch_nickname, "==> Failed")

  connect_to_branches_screen_detail_helper = PullDataHelper(uid='xxxx', pwd='xxxx', db_name='xxxxx')

  table_name = "[dbo].[branches_screen_detail]"
  db_con_awsp = connect_to_branches_screen_detail_helper.generate_dbconn('xxxx')
  
  if branch_nickname_failed:
    condition_sql = "[branch_nickname] NOT IN ({})".format("',' ".join(branch_nickname_failed))
    sql = connect_to_branches_screen_detail_helper.generate_sql_delete_with_condition(table_name, condition_sql)
    db_con_awsp.execute(sql)
  else:
    sql = connect_to_branches_screen_detail_helper.generate_sql_truncate(table_name)
    db_con_awsp.execute(sql)

  column_to_insert = "(branch_nickname, screen_number, screen_name)"
  batch_size = 5000
  for i in range(math.ceil(len(values_set_list) / batch_size)):
    sql = connect_to_branches_screen_detail_helper.generate_sql_insert(table_name=table_name, column_to_insert=column_to_insert, str_values_set_list=values_set_list[batch_size*i:batch_size*(i+1)])
    
    db_con_awsp.execute(sql)
    db_con_awsp.commit()
  return 
