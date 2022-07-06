from datetime import date, timedelta
from gevent import config
import config

DAY_G = config.DAY_G
MONTH_G = config.MONTH_G
YEAR_G = config.YEAR_G
NOVEMBER_ID = config.NOVEMBER_ID
DECEMBER_ID = config.DECEMBER_ID

def google_date(python_date_in_dash_format):
  _date = str(python_date_in_dash_format).split("-")
  return "/".join([
    _date[1],  # mm
    _date[2],  # dd
    _date[0]   # yy
  ])           # format to mm-dd-yyyy

def pdate(_date):
  try:
    _date = _date.split("/")
    return date(
      int(_date[2]),
      int(_date[0]),
      int(_date[1])
    )
  except Exception as err:
    e = f"ERR: cannot convert to python date: {err}"
    print(e)

def get_all_days_iso(dstart,dend,day_id_iso):
    dstart = pdate(dstart)
    dend = pdate(dend)
    days = [dstart + timedelta(days=x) for x in range((dend-dstart).days + 1) if (dstart + timedelta(days=x)).isoweekday() == day_id_iso]
    return days

def get_all_fridays_iso(dstart,dend):
    return get_all_days_iso(dstart,dend,config.FRIDAY)

def is_friday(_date):
  try:
    return pdate(_date).isoweekday() == config.FRIDAY
  except:
    print("ERR: cannot check friday")
    return False


def get_day_difference(date1,date2):
  try:
    return (pdate(date2) - pdate(date1)).days
  except:
    print("ERR: cannot check difference")
    return 0


def get_from_google_date(google_date,entitie_id):
  _date = google_date.split("/")
  return _date[entitie_id]


def is_november(google_date):
  month = get_from_google_date(google_date, MONTH_G)
  if str(month) == str(NOVEMBER_ID):
    return True

def is_december(google_date):
  month = get_from_google_date(google_date, MONTH_G)
  if month == DECEMBER_ID:
    return True


def years_matched(google_date1, google_date2):
  year1 = get_from_google_date(google_date1, YEAR_G)
  year2 = get_from_google_date(google_date2, YEAR_G)
  return year1 == year2