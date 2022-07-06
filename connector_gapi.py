import gspread
import config
import pandas as pd
from oauth2client.service_account import ServiceAccountCredentials


print("INITIALIZING PROGRAM")
scope = ['https://spreadsheets.google.com/feeds','https://www.googleapis.com/auth/drive']
creds = ServiceAccountCredentials.from_json_keyfile_name('c.json', scope)
client = gspread.authorize(creds)
sheet = None
sheet_dump = None
table_dump_counter = 0
update_cell_counter = 0

def dump_table(index=0):
    print(f"Dumping table N{index}: {table_dump_counter} times")
    sheet = client.open_by_key(config.TABLE_ID)
    sheet_dump = sheet.get_worksheet(index)
    return sheet_dump.get_all_records()


def update_cell(cellrange,data):
    print(f"Updateing cell {cellrange} : {update_cell_counter} times")
    sheet = client.open_by_key(config.TABLE_ID)
    sheet_dump = sheet.get_worksheet(0)
    return sheet_dump.update(cellrange,data)

