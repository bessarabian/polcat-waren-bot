# АЙДИ ТАБЛИЦЫ ----------------------------------------------------------------------.                         
#                                        |                                           |                         
# https://docs.google.com/spreadsheets/d/15X-Mho3Px4ZrRz15xR0hQ53KFsEGlJCzKpubFN3kgNk/edit#gid=1516304132      
TABLE_ID_TEST = '15X-Mho3Px4ZrRz15xR0hQ53KFsEGlJCzKpubFN3kgNk' 
TABLE_ID = '1TCyDrgMOz36fzNAxpDfcXeqb6pH4iKE_AmeilE15_nA'
BOT_FOLDER_ID_PROD="1uPd03Q0qqLGBVlJCaZGNe5DNz-gv_ci1" # ROOT FOLDER OF ALL DATA : BOT/*ТАБЛИЦЫ*ДОКУМЕНТЫ
TABLE_STARTS_AT="A"
TABLE_ENDS_AT="T"
TABLE_RANGE=f"{TABLE_STARTS_AT}:{TABLE_ENDS_AT}"
BAN_FRIDAYS_ID=1
BAN_FRIDAYS_KEY="BANNED FRIDAYS"
# Програмное 
SCOPES = ['https://www.googleapis.com/auth/spreadsheets.readonly']
TOKEN_FILE = "token.json"
CREDS_FILE = "c.json"


# TABLE SCHEMA
# Редактируя таблицу не забудьте обновить поля
###########
LOGIN="LOGIN"
PASSWORD="PASSWORD"	
PESEL_ID="PESEL ID"	
PASSPORT_ID	="PASSPORT ID"
TIMESTAMP="Timestamp"
END_VOCATION_DATE="Дата конца отпуска"
VISA_START_DATE="Дата начала визы"
CADENCE_START="Дата начала каденции"
CADENCE_END="Дата конца каденции"
ALL_DOCS="MANUAL"
DOCS="Документы"
MACRONA="Макрона"
А1="A1"
EKUZ="EKUZ"	
DEKLARACJE="DEKLARACJE"
Комментарий="Комментарий"
ID="ID"
STATUS="STATUS"
FOLDER_ID="FOLDER_ID" # FOLDER ID для маппинга таблиц

# Что хотите не показывать в боте
DONT_SHOW_THIS=[TIMESTAMP,PASSWORD,LOGIN,ID,STATUS,FOLDER_ID]

SAMPLE_SPREADSHEET_ID = TABLE_ID
SAMPLE_RANGE_NAME = TABLE_RANGE
DISABLE_FIELDS_FORMATTED=[""]
START_VOCATION_CELL = "I"
END_VOCATION_CELL = "J"
START_CONTRACT_DATE="Дата подисания договора"
START_VOCATION_DATE="Дата отпуска"
VISA_ENDS_DATE="Дата конца визы"
USER_PASSPORT_ID="PASSPORT ID"
USER_FULLNAME="Ф.И.О."

FRIDAY=5
DEV=False


MAX_FOLDERS_DEEPNES=1000


DAYS_IN_YEAR=365

#####
# КОЛИЧЕСТВО ЛЮДЕЙ НА ОДНУ КВОТУ
#####
MAX_EMPLOYES_PER_QUOTE=7


DAY_G = 1
MONTH_G = 0
YEAR_G = 2
NOVEMBER_ID = "11"
DECEMBER_ID = "12"
print("CONFIG READED")