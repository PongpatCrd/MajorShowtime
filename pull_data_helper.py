import pyodbc

def get_all_branch_server_ip():
  pull_data_helper = PullDataHelper(uid='xxxx', pwd='xxxx', db_name='xxxx')
  db_con = pull_data_helper.generate_dbconn('xxxx')

  column_name_list = ['[Branch_NickName]', '[Branch_Server]']
  table_name = "[dbo].[Tbl_Branch]"
  condition_sql = "[Branch_Server] IS NOT NULL AND [Branch_Status] = 1 AND [Branch_NoTheatre] > 0"

  sql = pull_data_helper.generate_sql_select_with_condition(column_name_list=column_name_list, table_name=table_name, where_case_sql=condition_sql)

  cursor = db_con.execute(sql)
  branch_server_ip_map = {detail.Branch_NickName: detail.Branch_Server for detail in cursor.fetchall()}
  return branch_server_ip_map

class PullDataHelper:
  def __init__(self, uid='xxxx', pwd='xxxx', db_name='xxxx'):
     self.uid = uid
     self.pwd = pwd
     self.db_name = db_name

  def generate_dbconn(self, branch_server_name):
    dbconn = pyodbc.connect(
      Driver   = '{SQL Server}',
      Server   = branch_server_name,
      Database = self.db_name,
      UID      = self.uid,
      PWD      = self.pwd
    )
    return dbconn

  def generate_sql_select(self, column_name_list, table_name):
    sql = "SELECT "

    column_name_list_last_idx = len(column_name_list) - 1
    for i in range(len(column_name_list)):
      if i < column_name_list_last_idx:
        sql += "{}, ".format(column_name_list[i])
      else:
        sql += "{} ".format(column_name_list[i])

    sql += "FROM {} WITH (NOLOCK)".format(table_name)
    return sql

  def generate_sql_select_with_condition(self, column_name_list, table_name, where_case_sql):
    sql = "SELECT "

    column_name_list_last_idx = len(column_name_list) - 1
    for i in range(len(column_name_list)):
      if i < column_name_list_last_idx:
        sql += "{}, ".format(column_name_list[i])
      else:
        sql += "{} ".format(column_name_list[i])

    sql += "FROM {} WITH (NOLOCK) WHERE {}".format(table_name, where_case_sql)
    return sql

  def generate_sql_insert(self, table_name, column_to_insert, str_values_set_list):
    sql = "INSERT INTO {} {} VALUES ".format(table_name, column_to_insert)

    values_set_list_last_idx = len(str_values_set_list) - 1
    for i in range(len(str_values_set_list)):
      if i < values_set_list_last_idx:
        sql += "{}, ".format(str_values_set_list[i])
      else:
        sql += "{} ".format(str_values_set_list[i])

    return sql
  
  def generate_sql_truncate(self, table_name):
    sql = "TRUNCATE TABLE {}".format(table_name)
    return sql

  def generate_sql_delete_with_condition(self, table_name, where_case_sql):
    sql = "DELETE FROM {} WHERE {}".format(table_name, where_case_sql)
    return sql