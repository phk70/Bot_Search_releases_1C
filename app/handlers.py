from annotated_types import T
from app.states import enter_version
from aiogram import Router, F
from aiogram.types import Message
from aiogram.filters import CommandStart
from aiogram.fsm.context import FSMContext
import app.keyboards as kb
import app.database.requests as req
from app.parse import check_version


router = Router()

@router.message(F.text == 'Назад')
async def back(message: Message, state: FSMContext):
    await state.clear()
    await message.answer('Выберите действие', reply_markup=kb.menu)


@router.message(CommandStart())
async def start_cmd(message: Message, state: FSMContext):    
    await state.set_state(enter_version.version)
    await message.answer(f'Привет, {message.from_user.first_name}!\nНачни работу с ввода версии в формате X.X.XXX.X')


# Отлавливаем первоначальную версию при первом запуске бота
@router.message(enter_version.version)
async def enter_version_in_sistem(message: Message, state: FSMContext):
    await state.update_data(version=message.text)
    version = await state.get_data()
    await req.save_version_in_db(version['version'])
    await message.reply(f'Версия {version['version']} сохранена', reply_markup=kb.menu)
    await state.clear()


@router.message(F.text == 'Текущая версия')
async def send_version(message: Message):    
    last_version = await req.get_last_version_from_db()    
    await message.reply(f'Текущая версия: {last_version.version}\nЗаписана: {last_version.create_data}')


@router.message(F.text == 'Ввести новую версию')
async def update_version(message: Message, state: FSMContext):
    await state.set_state(enter_version.version)
    await message.reply('Введите новую версию в формате X.X.XXX.X', reply_markup=kb.back) 


@router.message(enter_version.version)
async def update_version_in_sistem(message: Message, state: FSMContext):
    await state.update_data(version=message.text)
    version = await state.get_data()
    await req.save_version_in_db(version['version'])
    await message.reply(f'Версия {version['version']} сохранена', reply_markup=kb.menu)
    await state.clear()


@router.message(F.text == 'Проверить обновление')
async def send_version(message: Message):    
    check_version = await req.get_last_version_from_db()    
    await message.reply(f'Доступно обновление: {await check_version}, await check_version()')

'''
TODO 
Сделать кнопку отмена при состоянии ожидания.
Cделать рефакторинг  парсера
Подключить парсер к кнопке
Подумать над сем то еще, что улучшить
placeholderЫ на полу ввода на всех клавиатурах
'''