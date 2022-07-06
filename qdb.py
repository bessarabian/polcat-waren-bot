
print("QDB CORE INITED...")
users = {}


def get_all_records_amount():
  print(f"QDB records: {len(users)}")
  return len(users)

def save(user_tg_id,user_login_object):
  get_all_records_amount()
  print(f"QDB MESSAGE: saving {user_tg_id} object")
  try:
    users[user_tg_id] = user_login_object
    print(f"QDB MESSAGE: {user_tg_id} object saved")
    get_all_records_amount()
    return users
  except Exception as err:
    e = f"ERR IN QDB: cannot save user : {err}, data: {user_login_object}"
    print(e)
    get_all_records_amount()
    return e

def get(user_tg_id):
  print(f"QDB MESSAGE: getting {user_tg_id} object")
  try:
    if user_tg_id:
      return users[user_tg_id]
    print(f"ERR IN QDB: cannot get user, corrupted user id: {user_tg_id}")
  except Exception as err:
    e = f"ERR IN QDB: cannot get user : {err}, data: {user_tg_id}"
    print(e)
    return e


def drop():
  print("QDB CORE DROPPED, BYE!")