from aiogram.types import KeyboardButton, ReplyKeyboardMarkup

start_kb = ReplyKeyboardMarkup(keyboard=[[KeyboardButton(text='Ввести версию')]], 
                               resize_keyboard=True, input_field_placeholder='Введи версию в формате X.X.XXX.X')

menu = ReplyKeyboardMarkup(keyboard=[[KeyboardButton(text='Текущая версия')], 
                                     [KeyboardButton(text='Проверить обновление'), 
                                      KeyboardButton(text='Ввести новую версию')]], resize_keyboard=True)

back = ReplyKeyboardMarkup(keyboard=[[KeyboardButton(text='Назад')]], 
                           resize_keyboard=True)