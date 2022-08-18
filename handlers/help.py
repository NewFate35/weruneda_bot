from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.builtin import CommandHelp
from aiogram.dispatcher.filters.state import StatesGroup, State

from handlers.start import check
from handlers.start import IsAdmin
from keyboards import cancel_markup, markup_main_admin, markup_main
from loader import dp, bot, db


class Duo(StatesGroup):
    FIO = State()
    phone = State()


@dp.message_handler(text="27.08 20:30 забег с кофейней DUO")
async def start_duo_run(message: types.Message):
    await message.answer("Введите ваше ФИО:",
                         reply_markup=cancel_markup)
    await Duo.FIO.set()


@dp.message_handler(state=Duo.FIO)
async def save_duo_fio(message: types.Message, state: FSMContext):
    await state.update_data(fio=message.text)
    await message.answer("Введите ваш номер:")
    await Duo.phone.set()


@dp.message_handler(state=Duo.phone)
async def save_duo_phone(message: types.Message, state: FSMContext):
    duo_data = await state.get_data()
    fio = duo_data['fio']
    await db.add_user_duo_run(fio=fio, telegram_id=message.from_user.id, phone=message.text)
    if check(message.from_user.id):
        await message.answer("Спасибо за регистрацию!\nДо встречи в субботу 6.08 в 20:30 у входа БЦ Высоцкий🤍💙",
                             reply_markup=markup_main_admin)
    else:
        await message.answer("Спасибо за регистрацию!\nДо встречи в субботу 6.08 в 20:30 у входа БЦ Высоцкий🤍💙",
                             reply_markup=markup_main)

    await state.finish()


@dp.message_handler(IsAdmin(), text="Кол-во участников с DUO")
async def count(message: types.Message, state: FSMContext):
    count = await db.duo_count()
    await message.answer(f"Всего участников: {count}")
