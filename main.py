import asyncio
import logging
import config

from aiogram import Bot, Dispatcher
from aiogram.enums.parse_mode import ParseMode
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.utils.chat_action import ChatActionMiddleware
from handlers import router


async def main() -> None:
    # Initialize Bot instance with a default parse mode which will be passed to all API calls
    bot = Bot(config.BOT_TOKEN, parse_mode=ParseMode.HTML)
    # Dispatcher is a root router
    dp = Dispatcher(storage=MemoryStorage())
    # ... and all other routers should be attached to Dispatcher
    dp.include_router(router)

    # Middlewares
    dp.message.middleware(ChatActionMiddleware())
    await bot.delete_webhook(drop_pending_updates=True)
    # And the run events dispatching
    await dp.start_polling(bot)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    asyncio.run(main())
