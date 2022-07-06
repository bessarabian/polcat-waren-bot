import asyncio
from typing import Dict
import users_helper
import connector_gapi
import config
import qdb
from aiogram import Bot, Dispatcher, Router
from tg_token import TOKEN
from keyboard import *
from aiogram.dispatcher.fsm.context import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.types import Message, CallbackQuery
from callbacks import FridayCallback
from aiogram.dispatcher.fsm.storage.memory import MemoryStorage
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from aiogram.utils.keyboard import InlineKeyboardBuilder

router = Router()
storage = MemoryStorage()
API_TOKEN = TOKEN
bot = Bot(token=API_TOKEN, parse_mode="HTML")
dp = Dispatcher(storage=storage)
dp.include_router(router)
scheduler = AsyncIOScheduler()  
messages = []

async def delete_messages(chat_id):
    try:
        for msg in messages:
            await bot.delete_message(chat_id=chat_id, message_id=msg)
    except Exception as ex:
        print(ex)
    finally:
        messages.clear()

async def run_delete(chat_id):
    try:
        if scheduler.get_job('clearing'):
            scheduler.remove_job('clearing')
            scheduler.add_job(delete_messages, trigger="interval", hours=2, args=(chat_id,), id='clearing')
            scheduler.start()
        else:
            scheduler.add_job(delete_messages, trigger="interval", hours=2, args=(chat_id,), id='clearing')
            scheduler.start()
    except Exception as ex:
        print(ex)

class GetUserData(StatesGroup):
  usr_login = State()
  usr_password = State()

class GetVacationData(StatesGroup):
  start_vacation_data = State()
  end_vacation_data = State()

async def catch_updates(message: Message):
    messages.append(message.message_id)
    await run_delete(message.chat.id)

@dp.message(commands='start')
async def greeting(message: Message):
  await catch_updates(message)
  greet = await bot.send_message(message.chat.id, 'Приветствую!', reply_markup=start_kb)
  messages.append(greet.message_id)

@dp.message(text='Логин 🔑')
async def get_login(message: Message, state: FSMContext):
  await catch_updates(message)
  enter_login = await bot.send_message(message.chat.id, 'Введите ваш логин...')
  await state.set_state(GetUserData.usr_login)
  messages.append(enter_login.message_id)

@dp.message(GetUserData.usr_login)
async def process_get_login(message: Message, state: FSMContext):
  await catch_updates(message)
  await state.update_data(usr_login=message.text)
  await state.set_state(GetUserData.usr_password)
  enter_password = await bot.send_message(message.chat.id, 'Введите ваш пароль...')
  messages.append(enter_password.message_id)

@dp.message(state=GetUserData.usr_password)
async def process_get_password(message: Message, state: FSMContext):
  await catch_updates(message)
  data = await state.update_data(usr_password=message.text)
  await state.clear()
  result = await final_login(message.chat.id, message.from_user.id, data=data)
  await catch_updates(result)

async def final_login(chat_id, usr_id, data: Dict):
  user_data = users_helper.login(data.get('usr_login'), data.get('usr_password'))
  qdb.save(usr_id, user_data)
  if(user_data):
    msg = users_helper.get_formatted_message(user_data)
    print(qdb.get(usr_id))
    return await bot.send_message(chat_id, msg, reply_markup=control_kb)
  else:
    return await bot.send_message(usr_id, 'Произошла ошибка, проверьте данные для авторизации.')
    

@dp.message(text='Установить дату отпуска ✈️')
async def vacation_menu(message: Message):
  await catch_updates(message)
  _user_data = qdb.get(message.from_user.id)
  print(f"login({_user_data['LOGIN']},{_user_data['PASSWORD']})")
  user_data = users_helper.login(_user_data["LOGIN"], _user_data["PASSWORD"])
  print(f"user_data = {user_data}")
  qdb.save(message.from_user.id, user_data)
  print(user_data)
  try:
    if(len(users_helper.is_vocation_booked(user_data)) <= 1):
      try:
        banned_fridays = connector_gapi.dump_table(config.BAN_FRIDAYS_ID)
        builder = InlineKeyboardBuilder()
        for item in users_helper.get_all_fridays(user_data):
          if users_helper.is_valid_range(item, user_data) and not users_helper.is_friday_banned(item, banned_fridays):
            builder.button(
              text=item,
              callback_data=FridayCallback(date=item)
            )
            builder.adjust(3)
        available_fridays = await bot.send_message(message.chat.id, 'Доступные пятницы по датам:', reply_markup=builder.as_markup())
        messages.append(available_fridays.message_id)
      except Exception as ex:
        print(ex)
        errorchik = await bot.send_message(message.chat.id, 'Прозошла ошибка, обратитесь в тех. поддержку или администратору напрямую.')
        messages.append(errorchik.message_id)
    else:
      no_vacation = await bot.send_message(message.chat.id, 'Вы уже зарезервировали отпуск :(')
      messages.append(no_vacation.message_id)
  except Exception as ex:
    print(ex)
    error_msg = await bot.send_message(message.chat.id, 'Прозошла ошибка, обратитесь в тех. поддержку или администратору напрямую.')
    messages.append(error_msg.message_id)
  
@dp.callback_query(FridayCallback.filter())
async def get_vacation_cb(call: CallbackQuery, callback_data: FridayCallback):
  try:
    pyatnica = callback_data.date
    users_helper.REFRESH_TABLE_DUMP()
    _user_data = qdb.get(call.from_user.id)
    print(f"login({_user_data['LOGIN']},{_user_data['PASSWORD']})")
    user_data = users_helper.login(_user_data["LOGIN"], _user_data["PASSWORD"])
    print(f"user_data = {user_data}")
    qdb.save(call.from_user.id, user_data)
    print(f"all users: {qdb.users}")
    print(f"qdb getting : {qdb.get(call.from_user.id)}")
    users_helper.update_start_vocation_date(pyatnica, qdb.get(call.from_user.id))
    success_request = await bot.send_message(call.from_user.id, f'Отправлен запрос на установку даты отпуска на {pyatnica}!', reply_markup=control_kb)
    await catch_updates(success_request)
    messages.append(success_request.message_id)

  except Exception as ex:
    print(ex)
    error_msg = await bot.send_message(call.from_user.id, 'Прозошла ошибка, обратитесь в тех. поддержку или администратору напрямую.')
    messages.append(error_msg.message_id)

@dp.message(text='Справка ℹ️')
async def get_user_data(message: Message):
  await catch_updates(message)
  try:
    _user_data = qdb.get(message.from_user.id)
    user_data = users_helper.login(_user_data["LOGIN"], _user_data["PASSWORD"])
    print(f"user_data = {user_data}")
    qdb.save(message.from_user.id, user_data)
    msg = users_helper.get_formatted_message(user_data)
    await asyncio.sleep(0.3)
    control_msg = await bot.send_message(message.chat.id, msg, reply_markup=control_kb)
    await catch_updates(control_msg)
  except Exception as ex:
    print(ex)
    error_msg = await bot.send_message(message.chat.id, 'Прозошла ошибка, обратитесь в тех. поддержку или администратору напрямую.')
    await catch_updates(error_msg)

@dp.message(text='Мои документы 📚')
async def get_user_documents(message: Message):
  await catch_updates(message)
  try:
    document_kb = InlineKeyboardBuilder()
    document_kb.button(
      text='Ваши документы', 
      url = users_helper.get_folder_url(qdb.get(message.from_user.id))
    )
    answer = await bot.send_message(message.chat.id, 'Результат:', reply_markup=document_kb.as_markup())
    await catch_updates(answer)
  except Exception as err:
    print(err)
    error_msg = await bot.send_message(message.chat.id, 'Прозошла ошибка, обратитесь в тех. поддержку или администратору напрямую.')
    messages.append(error_msg.message_id)

@dp.message()
async def unknown_info(message: Message):
    await catch_updates(message)
    unkown = await bot.send_message(message.chat.id, "Что-то я вас не понял 0_o")
    messages.append(unkown.message_id)

if __name__ == "__main__":
    dp.run_polling(bot)