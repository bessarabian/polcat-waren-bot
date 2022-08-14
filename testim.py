from tg_token import TOKEN
from typing import Callable, Dict, Any, Awaitable
from aiogram import Bot, Dispatcher, BaseMiddleware, Router
from aiogram.dispatcher.filters import Command
from aiogram.types import Message
from apscheduler.schedulers.asyncio import AsyncIOScheduler

router = Router()
bot = Bot(token=TOKEN, parse_mode="HTML")
dp = Dispatcher()

messages = []
scheduler = AsyncIOScheduler()


class messageIdPickUp(BaseMiddleware):
    async def __call__(self, handler: Callable[[Message, Dict[str, Any]], Awaitable[Any]], event: Message, data: Dict[str, Any]) -> Any:
        print("Middleware triggered!")
        messages.append(event.message_id)
        try:
            if scheduler.get_job('clearing'):
                scheduler.remove_job('clearing')
                scheduler.add_job(clearing, trigger="interval", hours=1, args=(event,), id='clearing')
                scheduler.start()
            else:
                scheduler.add_job(clearing, trigger="interval", hours=1, args=(event,), id='clearing')
                scheduler.start()
        except Exception:
            pass
        return await handler(event, data)

async def clearing(message: Message):
    print("Clearing was started!")
    print(messages)
    for msg in messages:
        await bot.delete_message(message.chat.id, msg)
        print("Deleted message with ID: " + str(msg))
    print("Cleaning finished!")
    messages.clear()

router.message.outer_middleware(messageIdPickUp())

@router.message(Command(commands=['start']))
async def starting(message: Message):
    answer = await message.answer("ss")
    print(messages)
    messages.append(answer.message_id)


if __name__ == "__main__":
    dp.include_router(router)
    dp.run_polling(bot)