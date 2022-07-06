
from aiogram.dispatcher.filters.callback_data import CallbackData

class FridayCallback(CallbackData, prefix="friday"):
    date: str