
from aiogram import Bot, Dispatcher, executor, types
from aiogram.dispatcher.filters import Text

from main import *

import os


bot = Bot(token=os.getenv('TOKEN'))
dp = Dispatcher(bot)


@dp.message_handler(commands='start')
async def start(message: types.Message):
    start_buttons = ['Текущая версия', 'Проверить обновление']
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.add(*start_buttons)
    await message.answer('Выберите действие', reply_markup=keyboard)

    

@dp.message_handler(Text(equals='Текущая версия'))
async def send_version(message: types.Message):
    await message.answer(f'Текущая версия: {os.getenv("VERSION")}')

    
@dp.message_handler(Text(equals='Проверить обновление'))
async def send_version(message: types.Message):
    search_all_versions('list_base.html')
    await message.answer(serch_my_version(LIST_RELEASES, os.getenv('VERSION')))
    
    
def main():
    executor.start_polling(dp)

if __name__ == "__main__":
    main()
