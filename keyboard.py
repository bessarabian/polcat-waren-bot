import types
import aiogram
from aiogram.types.keyboard_button import KeyboardButton
from aiogram.types.reply_keyboard_markup import ReplyKeyboardMarkup


""" Reply Keyboard Buttons"""
login_btn = KeyboardButton(text='Логин 🔑')
get_data_btn = KeyboardButton(text='Справка ℹ️')
get_documents = KeyboardButton(text='Мои документы 📚')
vacation_btn = KeyboardButton(text='Установить дату отпуска ✈️')

""" Reply Keyboards Markups """
start_kb = ReplyKeyboardMarkup(keyboard=[[login_btn]], resize_keyboard=True, one_time_keyboard=True)#.row(login_btn)
control_kb = ReplyKeyboardMarkup(keyboard=[[get_data_btn], [get_documents], [vacation_btn]], resize_keyboard=True)#.row(get_data_btn)#.row(get_documents).row(vacation_btn)