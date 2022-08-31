from aiogram import types
from aiogram.dispatcher import FSMContext

import keyboards
from loader import dp, db, bot
from .training_states_group import Training


@dp.callback_query_handler(text="edit")
async def edit(call: types.CallbackQuery, state: FSMContext):
    res = await db.check_reg_status()
    if res['status']:
        await state.update_data(new_data=True)
        await bot.send_message(call.from_user.id, "Введите своё ФИО:", reply_markup=keyboards.cancel_markup)
        await call.message.edit_reply_markup()
        await Training.fullname.set()
    else:
        await bot.send_message(call.from_user.id, "Регистрация уже закрыта! Изменить информацию нельзя")
