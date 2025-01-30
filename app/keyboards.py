from aiogram.types import KeyboardButton, ReplyKeyboardMarkup

start_kb = ReplyKeyboardMarkup(keyboard=[[KeyboardButton(text='Ввести версию')]], 
                               resize_keyboard=True, input_field_placeholder='Введи версию в формате X.X.XXX.X')

menu = ReplyKeyboardMarkup(keyboard=[[KeyboardButton(text='Текущая версия'), 
                                      KeyboardButton(text='Проверить обновление')], 
                                      [KeyboardButton(text='Обновить версию')]], 
                               resize_keyboard=True)