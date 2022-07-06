from __future__ import print_function
from calendar import c
from datetime import date, datetime
from operator import ge

import os.path
from re import U
import config
import connector_gapi
import get_drive_files
import dates_helper

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

SCOPES = config.SCOPES
TOKEN_FILE = config.TOKEN_FILE
CREDS_FILE = config.CREDS_FILE
SAMPLE_SPREADSHEET_ID = config.TABLE_ID
SAMPLE_RANGE_NAME = config.TABLE_RANGE
START_VOCATION_CELL = config.START_VOCATION_CELL
END_VOCATION_CELL = config.END_VOCATION_CELL
START_CONTRACT_DATE=config.START_CONTRACT_DATE
START_VOCATION_DATE=config.START_VOCATION_DATE
USER_FULLNAME=config.USER_FULLNAME
USER_PASSPORT_ID=config.USER_PASSPORT_ID
VISA_ENDS_DATE=config.VISA_ENDS_DATE
FRIDAY=config.FRIDAY
DEV=config.DEV
DAYS_IN_YEAR=config.DAYS_IN_YEAR
MAX_EMPLOYES_PER_QUOTE=config.MAX_EMPLOYES_PER_QUOTE
TABLE_DUMP=connector_gapi.dump_table()

def REFRESH_TABLE_DUMP():
    try:
        TABLE_DUMP = connector_gapi.dump_table()
        return TABLE_DUMP
    except Exception as err:
        e = f"CANNOT REFRESH TABLE DUMP: {err}"
        print(e)
        return e

def login(uname,pwd):
  try:
    tdump = connector_gapi.dump_table()
    for u in tdump:
      if str(u["LOGIN"]) == str(uname):
        if str(u["PASSWORD"]) == str(pwd):
          _LOGIN_OBJECT = u
          return _LOGIN_OBJECT
  except Exception as err:
    e = f"CANNOT LOGIN: {err}, may be wrong password or user does not exists"
    print(e)
    return e

def REFRESH_LOGIN_OBJECT(LOGIN_OBJECT):
    try:
        user_name = LOGIN_OBJECT[config.LOGIN]
        user_password = LOGIN_OBJECT[config.PASSWORD]
        return login(user_name, user_password)
    except Exception as err:
        e = f"CANNOT REFRESH LOGIN DUMP: {err}"
        print(e)
        return e

def get_formatted_message(_LOGIN_OBJECT):
  try:
    counter = 0
    u = _LOGIN_OBJECT
    msg = ""
    if(u):
      for key in u:
        counter+=1
        if not key in config.DONT_SHOW_THIS and u[key]:
            print(key not in config.DONT_SHOW_THIS and u[key])
            msg += str(f"{key} -> `{u[key]}`\n\n")
    return msg
  except :
    e = "ERR: cannot format message: empty user or invalid password"
    print(e)
    return e

def is_friday_banned(friday_to_check,dump_fridays):
  try:
    all_fridays = []
    for friday in dump_fridays:
      all_fridays.append(friday[config.BAN_FRIDAYS_KEY])
    return friday_to_check in all_fridays
  except Exception as err:
    e = f"ERR: cannot check banned fridays: {err}"
    print(e)
    return e

def get_user_index(userObj,tableid=0):
  try:
    user_index = None
    _table_dump = TABLE_DUMP
    for _uobj in range(0, len(_table_dump)):
      print("----getting index condition")
      print(f"checking index for {userObj}")
      print(f"{userObj[config.PASSPORT_ID]} == {_table_dump[_uobj][config.PASSPORT_ID]}")
      if(userObj[config.PASSPORT_ID] == _table_dump[_uobj][config.PASSPORT_ID]):
        user_index = _uobj+2
    return user_index
  except Exception as err:
    print(f"ERR: cannot get user index: {err}")

def update_end_vocation_date(vocation_date,_LOGIN_OBJECT):
  try:  
    u = _LOGIN_OBJECT
    user_index = get_user_index(u)
    connector_gapi.update_cell(f"{END_VOCATION_CELL}{user_index}",vocation_date)
    return vocation_date
  except Exception as err:
    print(f"ERR: cannot update end vocation date: {err}")
    return False


def names_matched(doc_title,user_fullname):
  try:
    doc_title = doc_title.split("_")
    user_fullname = user_fullname.split(" ")
    passport_from_doc = doc_title[0]
    passport_from_user = user_fullname[0]
    name_from_doc_title = doc_title[1]
    user_name = user_fullname[1]
    if name_from_doc_title == user_name:
      surname_from_doc_title = doc_title[2]
      user_surname = user_fullname[2]
      if surname_from_doc_title == user_surname:
        if passport_from_doc == passport_from_user:
          return True
  except Exception as err:
    e = f"Cannot check user documents, crashed: {err}"


def google_drive_url(file_id):
  try:
    return f"https://drive.google.com/drive/u/0/folders/{file_id}/"
  except Exception as err:
    e = f"ERR: cannot convert google drive url {err}"
    print(e)
    return e

def how_many_employes_on_this_vocation_date(google_date):
  counter = 0
  for row in TABLE_DUMP:
    if row[START_VOCATION_DATE] == google_date:
      counter += 1
  return counter

def get_folder_url(_LOGIN_OBJECT):
  try:
    user = _LOGIN_OBJECT
    print(f"gettings urls done {_LOGIN_OBJECT}")
    return google_drive_url(_LOGIN_OBJECT[config.FOLDER_ID])
  except Exception as err:
    e = f"Cannot get urls of documents: {err}"
    print(e)
    return e

def is_valid_range(vocation_date,_LOGIN_OBJECT):
  try:
    u = _LOGIN_OBJECT
    start_working_at = u[START_CONTRACT_DATE]
    visa_ends_at = u[VISA_ENDS_DATE]
    visa_diff = dates_helper.get_day_difference(vocation_date,visa_ends_at)
    contract_diff = dates_helper.get_day_difference(start_working_at,vocation_date)
    today = dates_helper.google_date(datetime.today().strftime('%Y-%m-%d'))
    today_diff = dates_helper.get_day_difference(today,vocation_date)
    year_diff = dates_helper.get_day_difference(today,vocation_date)
    if dates_helper.is_friday(vocation_date):
      if visa_diff >= 14:
        if contract_diff >= 90:
          if today_diff >= 14:
            if dates_helper.years_matched(today,vocation_date):
              return True
            else:
              if dates_helper.is_november(today) or dates_helper.is_december(today):
                if year_diff <= DAYS_IN_YEAR:
                  return True
  except Exception as err:
    print(f"ERR: cannot check range validation: {err}")
    return False


def get_all_fridays(_LOGIN_OBJECT):
  try:
    print("Getting all fridays:")
    print(_LOGIN_OBJECT)
    result = []
    print("Start sorting fridays")
    user = _LOGIN_OBJECT
    from_date = user[START_CONTRACT_DATE]
    to_date = user[VISA_ENDS_DATE]
    fridays = dates_helper.get_all_fridays_iso(from_date,to_date)
    for friday in fridays:
      friday = dates_helper.google_date(friday)
      valid_range = is_valid_range(friday,user)
      if(valid_range):
        result.append(friday)
    print("Done!")
    return result
  except Exception as err:
    print(f"ERR: cannot get all fridays missed required data to calculate: {err}", _LOGIN_OBJECT)
    return False

def update_start_vocation_date(vocation_date,_LOGIN_OBJECT):
  try:
    if how_many_employes_on_this_vocation_date(vocation_date) <= MAX_EMPLOYES_PER_QUOTE:  
      u = _LOGIN_OBJECT
      user_index = get_user_index(u)
      cell_id = f"{START_VOCATION_CELL}{user_index}"
      connector_gapi.update_cell(cell_id,vocation_date)
      TABLE_DUMP = connector_gapi.dump_table()
    else:
      return "ERR: 10 employes already on this quote"
  except Exception as err:
    e = f"ERR: cannot update start vocation date: {err}"
    print(e)
    return e

def is_vocation_booked(_LOGIN_OBJECT):
  return _LOGIN_OBJECT[config.START_VOCATION_DATE]