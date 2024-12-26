
from aiogram import Bot, Dispatcher, executor, types
from aiogram.dispatcher.filters import Text
from dotenv import load_dotenv
from main import login, view_version, save_version, search_all_versions, serch_up_for_my_version
import time

import os
load_dotenv()


bot = Bot(token=os.getenv('TOKEN'))
dp = Dispatcher(bot)


# Стартовое меню
@dp.message_handler(commands='start')
async def start(message: types.Message): 
    start_buttons = ['Текущая версия', 'Проверить обновление', 'Обновить версию']
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True, input_field_placeholder="")
    keyboard.add(*start_buttons)
    await message.answer('Выберите действие', reply_markup=keyboard)


# Нажатие на кнопку Текущая версия
@dp.message_handler(Text(equals='Текущая версия'))
async def send_version(message: types.Message):    
    await message.answer(f'Текущая версия: {view_version()}')


# Нажатие на кнопку Проверить обновление
@dp.message_handler(Text(equals='Проверить обновление'))
async def search_updates(message: types.Message):
    login(os.getenv('URL'), os.getenv('LOGIN'), os.getenv('PASSWORD'))   
    search_all_versions('list_base.html')
    await message.answer(serch_up_for_my_version('list_releases.json'))


# Нажатие на кнопку Обновить версию
@dp.message_handler(Text(equals='Обновить версию'))
async def update_version_in_sistem(message: types.Message): 
    up_kb = ["Назад"]
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True, input_field_placeholder="")
    keyboard.add(*up_kb)
    await message.answer('Введите новую версию в формате X.X.XXX.X', reply_markup=keyboard)


@dp.message_handler()
async def update_version_in_sistem(message: types.Message):         
    new_version = message.text
    save_version(new_version)
    await message.answer('Версия обновлена')


# Нажатие на кнопку Назад
@dp.message_handler(Text(equals='Назад'))
async def back(message: types.Message): 
    start_buttons = ['Текущая версия', 'Проверить обновление', 'Обновить версию']
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True, input_field_placeholder="")
    keyboard.add(*start_buttons)
    await message.answer('Выберите действие', reply_markup=keyboard)


def main():
    executor.start_polling(dp)

if __name__ == "__main__":
    main()
