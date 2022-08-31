from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import StatesGroup, State

import keyboards
from loader import dp, db


class Duo(StatesGroup):
    FIO = State()
    phone = State()


@dp.message_handler(text="24.09 20:30 забег с кофейней DUO")
async def start_duo_run(message: types.Message):
    await message.answer("Введите ваше ФИО:",
                         reply_markup=keyboards.cancel_markup)
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
    await message.answer("Спасибо за регистрацию!\nДо встречи в субботу 24.09 в 20:30 у входа БЦ Высоцкий🤍💙",
                         reply_markup=keyboards.main_markup(message.from_user.id))

    await state.finish()
