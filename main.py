import asyncio
import os
import logging
from aiogram import Bot, Dispatcher
from app.database.models import create_all_tables
from app.handlers import router
from dotenv import load_dotenv

load_dotenv()


async def main():
    await create_all_tables()
    logging.basicConfig(level=logging.INFO)    
    bot = Bot(token=os.getenv('BOT_TOKEN'))
    dp = Dispatcher()
    dp.include_router(router)
    await dp.start_polling(bot)
    

if __name__ == '__main__':
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print('Завершение работы бота')