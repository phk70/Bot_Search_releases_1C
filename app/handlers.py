from app.states import enter_version
from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.filters import Command, CommandStart
from aiogram.fsm.context import FSMContext
import app.keyboards as kb
import app.database.requests as req


router = Router()


@router.message(CommandStart())
async def start_cmd(message: Message, state: FSMContext):
    await state.set_state(enter_version.version)
    await message.answer(f'Привет, {message.from_user.first_name}!\nНачни работу с ввода версии в формате X.X.XXX.X')


# Отлавливаем первоначальную версию при первом запуске бота
@router.message(enter_version.version)
async def enter_version_in_sistem(message: Message, state: FSMContext):
    await state.update_data(version=message.text)
    version = await state.get_data()
    print(version)    
    print(version['version'])
    print(type(version['version']))
    version = version['version']
    await req.save_version_in_db(version)
    await message.answer('Версия сохранена', reply_markup=kb.menu)
    await state.clear()