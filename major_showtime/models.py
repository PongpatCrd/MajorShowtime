from django.db import models
from django.utils.timezone import now

# Create your models here.

# major_showtime (default)
class MovieEstimatedIncome(models.Model):
  id = models.AutoField(primary_key=True)
  mv_id = models.IntegerField(blank=False, null=False)
  income_estimated = models.PositiveSmallIntegerField(default=0, blank=False, null=False)

  class Meta:
    db_table = "movie_estimated_income"
    indexes = [
      models.Index(fields=['mv_id']),
    ]

class BranchesBestTimeDetail(models.Model):
  id              = models.AutoField(primary_key=True)
  branch_nickname = models.CharField(max_length=5, blank=False, null=False)
  best_time       = models.CharField(max_length=5, blank=False, null=False)
  is_active       = models.BooleanField(default=True)
  created_at      = models.DateTimeField(default=now, editable=False)
  updated_at      = models.DateTimeField(auto_now=True)

  class Meta:
    db_table = 'branches_best_time_detail'
    index_together = [
      ['branch_nickname', 'is_active'],
      ['branch_nickname', 'created_at'],
      ['branch_nickname', 'is_active', 'created_at'],
    ]

class BranchesTimeSetting(models.Model):
  id                 = models.AutoField(primary_key=True)
  branch_nickname    = models.CharField(max_length=5, blank=False, null=False)
  first_showtime     = models.CharField(max_length=5, blank=False, null=False)
  last_showtime      = models.CharField(max_length=5, blank=False, null=False)
  advertisement_time = models.PositiveSmallIntegerField(default=0, blank=False, null=False)
  clean_up_time      = models.PositiveSmallIntegerField(default=0, blank=False, null=False)
  break_time         = models.PositiveSmallIntegerField(default=0, blank=False, null=False)
  is_active          = models.BooleanField(default=True)
  created_at         = models.DateTimeField(default=now, editable=False)
  updated_at         = models.DateTimeField(auto_now=True)

  class Meta:
    db_table = "branches_time_setting"
    index_together = [
      ['branch_nickname', 'is_active'],
      ['branch_nickname', 'created_at'],
      ['branch_nickname', 'updated_at'],
      ['branch_nickname', 'created_at', 'is_active'],
      ['branch_nickname', 'updated_at', 'is_active']
    ]

class BranchesScreenDetail(models.Model):
  id              = models.AutoField(primary_key=True)
  branch_nickname = models.CharField(max_length=5, blank=False, null=False)
  screen_number   = models.PositiveSmallIntegerField(blank=False, null=False)
  screen_name     = models.CharField(max_length=40, blank=True, null=True)
  n_seat          = models.PositiveSmallIntegerField(null=True)
  
  class Meta:
    db_table = "branches_screen_detail"
    index_together = [
      ['branch_nickname', 'screen_number'],
      ['branch_nickname', 'screen_name'],
      ['branch_nickname', 'screen_number', 'screen_name']
    ]

class BranchesRegionSetting(models.Model):
  id                = models.AutoField(primary_key=True)
  branch_nickname   = models.CharField(max_length=5, blank=False, null=False)
  branch_code_vista = models.CharField(max_length=5, blank=False, null=True, default=None)
  branch_region     = models.CharField(max_length=20, blank=False, null=True, default=None)

  class Meta:
    db_table = "branches_region_setting"

# ticket_sale
class TblMv(models.Model):
  mv_id = models.IntegerField(db_column='MV_ID', primary_key=True)  # Field name made lowercase.
  mv_ename = models.CharField(db_column='MV_Ename', max_length=100, blank=True, null=True)  # Field name made lowercase.
  mv_tname = models.CharField(db_column='MV_Tname', max_length=100, blank=True, null=True)  # Field name made lowercase.
  mv_kname = models.CharField(db_column='MV_Kname', max_length=100, blank=True, null=True)  # Field name made lowercase.
  mv_sname = models.CharField(db_column='MV_Sname', max_length=20, blank=True, null=True)  # Field name made lowercase.
  mv_actor = models.CharField(db_column='MV_Actor', max_length=100, blank=True, null=True)  # Field name made lowercase.
  mv_actress = models.CharField(db_column='MV_Actress', max_length=100, blank=True, null=True)  # Field name made lowercase.
  distributor_id = models.IntegerField(db_column='Distributor_ID', blank=True, null=True)  # Field name made lowercase.
  mv_time = models.IntegerField(db_column='MV_Time', blank=True, null=True)  # Field name made lowercase.
  mv_adtime = models.IntegerField(db_column='MV_AdTime', blank=True, null=True)  # Field name made lowercase.
  mv_releasedate = models.CharField(db_column='MV_ReleaseDate', max_length=8, blank=True, null=True)  # Field name made lowercase.
  mv_expiredate = models.CharField(db_column='MV_ExpireDate', max_length=8, blank=True, null=True)  # Field name made lowercase.
  mv_desc = models.CharField(db_column='MV_Desc', max_length=255, blank=True, null=True)  # Field name made lowercase.
  mv_abstract = models.CharField(db_column='MV_Abstract', max_length=255, blank=True, null=True)  # Field name made lowercase.
  mv_status = models.SmallIntegerField(db_column='MV_Status', blank=True, null=True)  # Field name made lowercase.
  lastupdate = models.DateTimeField(db_column='LastUpdate', blank=True, null=True)  # Field name made lowercase.
  mv_groupid = models.IntegerField(db_column='MV_GroupID', blank=True, null=True)  # Field name made lowercase.
  mvnation_id = models.CharField(db_column='MVNation_ID', max_length=2, blank=True, null=True)  # Field name made lowercase.
  mvgenre_id = models.SmallIntegerField(db_column='MVGenre_ID', blank=True, null=True)  # Field name made lowercase.

  class Meta:
    managed = False
    db_table = 'tbl_mv'

class TblMvformat(models.Model):
  format_strcode = models.CharField(db_column='Format_strCode', primary_key=True, max_length=10)  # Field name made lowercase.
  format_strname = models.CharField(db_column='Format_strName', max_length=30, blank=True, null=True)  # Field name made lowercase.
  format_strshortname = models.CharField(db_column='Format_strShortName', max_length=15, blank=True, null=True)  # Field name made lowercase.
  format_strisdigital = models.CharField(db_column='Format_strIsDigital', max_length=1, blank=True, null=True)  # Field name made lowercase.
  format_strdefault = models.CharField(db_column='Format_strDefault', max_length=1, blank=True, null=True)  # Field name made lowercase.
  stype_strsessiontypecode = models.CharField(db_column='SType_strSessionTypeCode', max_length=10)  # Field name made lowercase.
  format_strstatus = models.CharField(db_column='Format_strStatus', max_length=1, blank=True, null=True)  # Field name made lowercase.
  hopk = models.CharField(db_column='HOPK', max_length=10, blank=True, null=True)  # Field name made lowercase.
  format_dtmlastmodifieddate = models.DateTimeField(db_column='Format_dtmLastModifiedDate', blank=True, null=True)  # Field name made lowercase.
  format_strnamealt = models.CharField(db_column='Format_strNameAlt', max_length=30, blank=True, null=True)  # Field name made lowercase.
  format_strshortnamealt = models.CharField(db_column='Format_strShortNameAlt', max_length=10, blank=True, null=True)  # Field name made lowercase.
  glaccount_strid = models.CharField(db_column='GLAccount_strID', max_length=10, blank=True, null=True)  # Field name made lowercase.
  format_strnamealt2 = models.CharField(db_column='Format_strNameAlt2', max_length=30, blank=True, null=True)  # Field name made lowercase.
  format_strnamealt3 = models.CharField(db_column='Format_strNameAlt3', max_length=30, blank=True, null=True)  # Field name made lowercase.
  format_strshortnamealt2 = models.CharField(db_column='Format_strShortNameAlt2', max_length=10, blank=True, null=True)  # Field name made lowercase.
  format_strshortnamealt3 = models.CharField(db_column='Format_strShortNameAlt3', max_length=10, blank=True, null=True)  # Field name made lowercase.

  class Meta:
    managed = False
    db_table = 'tbl_mvformat'

class TblMvformatdetail(models.Model):
  mv_id = models.IntegerField(db_column='MV_ID')  # Field name made lowercase.
  format_strcode = models.CharField(db_column='Format_strCode', max_length=100, blank=True, null=True)  # Field name made lowercase.
  createdate = models.DateTimeField(db_column='CreateDate', blank=True, null=True)  # Field name made lowercase.

  class Meta:
    managed = False
    db_table = 'tbl_MVFormatDetail'

class TblMvgenre(models.Model):
  mvgenre_id = models.SmallIntegerField(db_column='MVGenre_ID', blank=True, null=True)  # Field name made lowercase.
  mvgenre_ename = models.CharField(db_column='MVGenre_EName', max_length=50, blank=True, null=True)  # Field name made lowercase.
  mvgenre_tname = models.CharField(db_column='MVGenre_TName', max_length=50, blank=True, null=True)  # Field name made lowercase.

  class Meta:
    managed = False
    db_table = 'tbl_MVGenre'

class TblMvlanguage(models.Model):
  mvlang_id = models.IntegerField(db_column='MvLang_ID', primary_key=True)  # Field name made lowercase.
  mvlang_ename = models.CharField(db_column='MvLang_EName', max_length=20, blank=True, null=True)  # Field name made lowercase.
  mvlang_tname = models.CharField(db_column='MvLang_TName', max_length=20, blank=True, null=True)  # Field name made lowercase.
  lastupdate = models.DateTimeField(db_column='LastUpdate', blank=True, null=True)  # Field name made lowercase.

  class Meta:
    managed = False
    db_table = 'tbl_MVLanguage'

class TblMvnation(models.Model):
  mvnation_id = models.CharField(db_column='MVNation_ID', max_length=2, blank=True, null=True)  # Field name made lowercase.
  mvnation_ename = models.CharField(db_column='MVNation_EName', max_length=50, blank=True, null=True)  # Field name made lowercase.
  mvnation_tname = models.CharField(db_column='MVNation_TName', max_length=50, blank=True, null=True)  # Field name made lowercase.

  class Meta:
    managed = False
    db_table = 'tbl_MVNation'

class TblMvprogram(models.Model):
  branch_id = models.CharField(db_column='Branch_ID', primary_key=True, max_length=3)  # Field name made lowercase.
  theatre = models.IntegerField(db_column='Theatre')  # Field name made lowercase.
  program_date = models.CharField(db_column='Program_Date', max_length=8)  # Field name made lowercase.
  program_time = models.CharField(db_column='Program_Time', max_length=5)  # Field name made lowercase.
  mv_id = models.IntegerField(db_column='MV_ID', blank=True, null=True)  # Field name made lowercase.
  mvlang_id = models.IntegerField(db_column='MvLang_ID', blank=True, null=True)  # Field name made lowercase.
  lastupdate = models.DateTimeField(db_column='LastUpdate', blank=True, null=True)  # Field name made lowercase.
  ipupdate = models.CharField(db_column='IPUpdate', max_length=20, blank=True, null=True)  # Field name made lowercase.
  program_fix = models.SmallIntegerField(db_column='Program_Fix', blank=True, null=True)  # Field name made lowercase.
  format_strcode = models.CharField(db_column='Format_strCode', max_length=10, blank=True, null=True)  # Field name made lowercase.

  class Meta:
    managed = False
    db_table = 'tbl_MVProgram'
    unique_together = (('branch_id', 'theatre', 'program_date', 'program_time'),)

class TblMvshowtime(models.Model):
  branch_nickname = models.CharField(db_column='Branch_Nickname', max_length=50)  # Field name made lowercase.
  theatre = models.IntegerField(db_column='Theatre')  # Field name made lowercase.
  program_date = models.CharField(db_column='Program_Date', max_length=8)  # Field name made lowercase.
  program_time = models.CharField(db_column='Program_Time', max_length=5)  # Field name made lowercase.
  sessionid = models.CharField(db_column='SessionID', max_length=50)  # Field name made lowercase.
  mv_id = models.CharField(db_column='MV_ID', max_length=50)  # Field name made lowercase.
  movieename = models.CharField(db_column='MovieEName', max_length=100)  # Field name made lowercase.
  movietname = models.CharField(db_column='MovieTName', max_length=100)  # Field name made lowercase.
  moviesname = models.CharField(db_column='MovieSName', max_length=50)  # Field name made lowercase.
  moviescode = models.CharField(db_column='MovieSCode', max_length=50, blank=True, null=True)  # Field name made lowercase.
  movielang = models.CharField(db_column='MovieLang', max_length=50)  # Field name made lowercase.
  sessiondate = models.CharField(db_column='SessionDate', max_length=8)  # Field name made lowercase.
  status = models.CharField(db_column='Status', max_length=5, blank=True, null=True)  # Field name made lowercase.
  flagvista_box = models.IntegerField(db_column='FlagVista_Box', blank=True, null=True)  # Field name made lowercase.
  createdate = models.DateTimeField(db_column='CreateDate', blank=True, null=True)  # Field name made lowercase.
  channel = models.CharField(db_column='Channel', max_length=255, blank=True, null=True)  # Field name made lowercase.

  class Meta:
    managed = False
    db_table = 'tbl_MVShowtime'

class TblSummovieseatnew(models.Model):
  datesum = models.CharField(db_column='DateSum', max_length=8, blank=True, null=True)  # Field name made lowercase.
  branchid = models.CharField(db_column='BranchID', max_length=2, blank=True, null=True)  # Field name made lowercase.
  mvname = models.CharField(db_column='MvName', max_length=150, blank=True, null=True)  # Field name made lowercase.
  theatre = models.IntegerField(db_column='Theatre', blank=True, null=True)  # Field name made lowercase.
  rdtime = models.CharField(db_column='RdTime', max_length=5, blank=True, null=True)  # Field name made lowercase.
  seattypeid = models.CharField(db_column='SeatTypeID', max_length=10, blank=True, null=True)  # Field name made lowercase.
  admis = models.IntegerField(db_column='Admis', blank=True, null=True)  # Field name made lowercase.
  ticket = models.IntegerField(db_column='Ticket', blank=True, null=True)  # Field name made lowercase.
  service = models.IntegerField(db_column='Service', blank=True, null=True)  # Field name made lowercase.
  comfee = models.IntegerField(db_column='ComFee', blank=True, null=True)  # Field name made lowercase.
  seat = models.IntegerField(db_column='Seat', blank=True, null=True)  # Field name made lowercase.
  seattypename = models.CharField(db_column='SeatTypeName', max_length=50, blank=True, null=True)  # Field name made lowercase.

  class Meta:
    managed = False
    db_table = 'tbl_SumMovieSeatNew'

class TblBranch(models.Model):
  id = models.IntegerField(db_column='ID', primary_key=True)  # Field name made lowercase.
  branch_id = models.CharField(db_column='Branch_ID', max_length=2)  # Field name made lowercase.
  complex_id = models.IntegerField(db_column='Complex_ID', blank=True, null=True)  # Field name made lowercase.
  complex_name = models.CharField(db_column='Complex_Name', max_length=50, blank=True, null=True)  # Field name made lowercase.
  complex_order = models.IntegerField(db_column='Complex_Order', blank=True, null=True)  # Field name made lowercase.
  branchcodevista = models.CharField(db_column='BranchCodeVista', max_length=5, blank=True, null=True)  # Field name made lowercase.
  branch_fullname = models.CharField(db_column='Branch_FullName', max_length=30)  # Field name made lowercase.
  branch_thainame = models.CharField(db_column='Branch_ThaiName', max_length=30, blank=True, null=True)  # Field name made lowercase.
  branch_nickname = models.CharField(db_column='Branch_NickName', max_length=3, blank=True, null=True)  # Field name made lowercase.
  branch_callname = models.CharField(db_column='Branch_CallName', max_length=100, blank=True, null=True)  # Field name made lowercase.
  branch_server = models.CharField(db_column='Branch_Server', max_length=25, blank=True, null=True)  # Field name made lowercase.
  branch_trans = models.CharField(db_column='Branch_Trans', max_length=50, blank=True, null=True)  # Field name made lowercase.
  branch_group = models.IntegerField(db_column='Branch_Group', blank=True, null=True)  # Field name made lowercase.
  branch_program = models.CharField(db_column='Branch_Program', max_length=50, blank=True, null=True)  # Field name made lowercase.
  branch_dbuser = models.CharField(db_column='Branch_DbUser', max_length=50, blank=True, null=True)  # Field name made lowercase.
  branch_dbpass = models.CharField(db_column='Branch_DbPass', max_length=50, blank=True, null=True)  # Field name made lowercase.
  branch_dbname = models.CharField(db_column='Branch_DbName', max_length=50, blank=True, null=True)  # Field name made lowercase.
  branch_dbtype = models.SmallIntegerField(db_column='Branch_DbType', blank=True, null=True)  # Field name made lowercase.
  branch_notheatre = models.IntegerField(db_column='Branch_NoTheatre', blank=True, null=True)  # Field name made lowercase.
  branch_noseat = models.IntegerField(db_column='Branch_NoSeat', blank=True, null=True)  # Field name made lowercase.
  branch_nolane = models.IntegerField(db_column='Branch_NoLane', blank=True, null=True)  # Field name made lowercase.
  branch_noroom = models.IntegerField(db_column='Branch_NoRoom', blank=True, null=True)  # Field name made lowercase.
  branch_nobox = models.IntegerField(db_column='Branch_NoBox', blank=True, null=True)  # Field name made lowercase.
  branch_notable = models.IntegerField(db_column='Branch_NoTable', blank=True, null=True)  # Field name made lowercase.
  branch_noice = models.IntegerField(db_column='Branch_NoIce', blank=True, null=True)  # Field name made lowercase.
  branch_orderbox = models.IntegerField(db_column='Branch_OrderBox', blank=True, null=True)  # Field name made lowercase.
  branch_orderbow = models.IntegerField(db_column='Branch_OrderBow', blank=True, null=True)  # Field name made lowercase.
  branch_db = models.CharField(db_column='Branch_DB', max_length=50, blank=True, null=True)  # Field name made lowercase.
  branch_performancelocation = models.CharField(db_column='Branch_PerformanceLocation', max_length=50, blank=True, null=True)  # Field name made lowercase.
  branch_location = models.CharField(db_column='Branch_Location', max_length=50, blank=True, null=True)  # Field name made lowercase.
  branch_zone = models.CharField(db_column='Branch_Zone', max_length=50, blank=True, null=True)  # Field name made lowercase.
  branch_region = models.CharField(db_column='Branch_Region', max_length=50, blank=True, null=True)  # Field name made lowercase.
  branch_conprice = models.CharField(db_column='Branch_ConPrice', max_length=50, blank=True, null=True)  # Field name made lowercase.
  branch_ename = models.CharField(db_column='Branch_EName', max_length=25, blank=True, null=True)  # Field name made lowercase.
  branch_tname = models.CharField(db_column='Branch_TName', max_length=50, blank=True, null=True)  # Field name made lowercase.
  branch_mjbname = models.CharField(db_column='Branch_MJBName', max_length=3, blank=True, null=True)  # Field name made lowercase.
  branch_nickconcert = models.CharField(db_column='Branch_NickConcert', max_length=6, blank=True, null=True)  # Field name made lowercase.
  branch_boxcompany = models.SmallIntegerField(db_column='Branch_BoxCompany', blank=True, null=True)  # Field name made lowercase.
  branch_ipbowl = models.CharField(db_column='Branch_IPBowl', max_length=15, blank=True, null=True)  # Field name made lowercase.
  branch_ipconc = models.CharField(db_column='Branch_IPConc', max_length=15, blank=True, null=True)  # Field name made lowercase.
  branch_ipbowluser = models.CharField(db_column='Branch_IPBowlUser', max_length=50, blank=True, null=True)  # Field name made lowercase.
  branch_ipbowlpass = models.CharField(db_column='Branch_IPBowlPass', max_length=50, blank=True, null=True)  # Field name made lowercase.
  branch_dbbowl = models.CharField(db_column='Branch_DBBowl', max_length=50, blank=True, null=True)  # Field name made lowercase.
  branch_dbconc = models.CharField(db_column='Branch_DBConc', max_length=50, blank=True, null=True)  # Field name made lowercase.
  branch_groupbow = models.SmallIntegerField(db_column='Branch_GroupBow', blank=True, null=True)  # Field name made lowercase.
  branch_status = models.SmallIntegerField(db_column='Branch_Status', blank=True, null=True)  # Field name made lowercase.
  branch_bowversion = models.CharField(db_column='Branch_BowVersion', max_length=15, blank=True, null=True)  # Field name made lowercase.
  branch_bowlink = models.CharField(db_column='Branch_BowLink', max_length=15, blank=True, null=True)  # Field name made lowercase.
  branch_locationmjc = models.CharField(db_column='Branch_LocationMJC', max_length=3, blank=True, null=True)  # Field name made lowercase.
  branch_open = models.CharField(db_column='Branch_Open', max_length=8, blank=True, null=True)  # Field name made lowercase.
  branch_close = models.CharField(db_column='Branch_Close', max_length=8, blank=True, null=True)  # Field name made lowercase.
  branch_openbow = models.CharField(db_column='Branch_OpenBow', max_length=8, blank=True, null=True)  # Field name made lowercase.
  branch_contributelocation = models.CharField(db_column='Branch_ContributeLocation', max_length=3, blank=True, null=True)  # Field name made lowercase.
  branch_ipbms = models.CharField(db_column='Branch_IPBMS', max_length=50, blank=True, null=True)  # Field name made lowercase.
  branchivrstatus = models.CharField(db_column='BranchIVRStatus', max_length=10, blank=True, null=True)  # Field name made lowercase.
  con_email = models.CharField(db_column='Con_Email', max_length=100, blank=True, null=True)  # Field name made lowercase.
  bow_status = models.SmallIntegerField(db_column='Bow_Status', blank=True, null=True)  # Field name made lowercase.
  directlineno = models.CharField(db_column='DirectLineNo', max_length=50, blank=True, null=True)  # Field name made lowercase.
  directline_server = models.CharField(db_column='DirectLine_Server', max_length=50, blank=True, null=True)  # Field name made lowercase.
  branch_vistadate = models.CharField(db_column='Branch_VISTADate', max_length=8, blank=True, null=True)  # Field name made lowercase.
  bow_area = models.CharField(db_column='Bow_Area', max_length=10, blank=True, null=True)  # Field name made lowercase.
  branch_servername = models.CharField(db_column='Branch_ServerName', max_length=50, blank=True, null=True)  # Field name made lowercase.
  kiosk_qty = models.SmallIntegerField(db_column='Kiosk_Qty', blank=True, null=True)  # Field name made lowercase.
  kiosk_std = models.SmallIntegerField(db_column='Kiosk_Std', blank=True, null=True)  # Field name made lowercase.
  kiosk_pro = models.SmallIntegerField(db_column='Kiosk_Pro', blank=True, null=True)  # Field name made lowercase.
  kiosk_photo = models.SmallIntegerField(db_column='Kiosk_Photo', blank=True, null=True)  # Field name made lowercase.
  branch_kiosksaleservername = models.CharField(db_column='Branch_KioskSaleServerName', max_length=50, blank=True, null=True)  # Field name made lowercase.

  class Meta:
    managed = False
    db_table = 'Tbl_Branch'
    unique_together = (('id', 'branch_id'),)

class TblDistributor(models.Model):
  distributor_id = models.IntegerField(db_column='Distributor_ID')  # Field name made lowercase.
  distributor_name = models.CharField(db_column='Distributor_Name', max_length=50, blank=True, null=True)  # Field name made lowercase.
  distributor_addr = models.CharField(db_column='Distributor_Addr', max_length=100, blank=True, null=True)  # Field name made lowercase.
  distributor_tel = models.CharField(db_column='Distributor_Tel', max_length=20, blank=True, null=True)  # Field name made lowercase.
  distributor_status = models.SmallIntegerField(db_column='Distributor_Status', blank=True, null=True)  # Field name made lowercase.
  lastupdate = models.DateTimeField(db_column='LastUpdate', blank=True, null=True)  # Field name made lowercase.

  class Meta:
    managed = False
    db_table = 'tbl_Distributor'