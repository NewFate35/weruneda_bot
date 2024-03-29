from aiogram import types
from aiogram.dispatcher import FSMContext

from handlers.users.start import check_admin
import keyboards
from loader import dp, db, bot
from ..training_states_group import Training


@dp.callback_query_handler(text="without_breakfast", state=Training.breakfast)
async def without_breakfast(call: types.CallbackQuery, state: FSMContext):
    reg_data = await state.get_data()
    user_id = call.from_user.id
    fullname = reg_data['FIO']
    phone = reg_data['phone']

    if reg_data['new_data']:
        await db.add_or_update_user_data(call.from_user.id, fullname, phone)
    await db.add_user_training(user_id, fullname, phone, meat_count=0, vegan_count=0)

    await bot.send_message(call.from_user.id,
                           text=f"ФИО: {fullname}\nТелефон: {phone}\n"
                                f"Успешная регистрация на тренировку без завтрака!",
                           reply_markup=keyboards.edit_keyboard)

    await bot.send_message(call.from_user.id,
                           text="➡️Оплата переводом по номеру: +7-912-618-19-37 (Сбербанк/Тинькофф)"
                                "\nВ назначении платежа указывайте фамилию"
                                "\n\nТренировка + завтрак - 400₽"
                                "\nГрупповая тренировка - 100₽",
                           reply_markup=keyboards.main_markup(call.from_user.id))
    await call.message.edit_reply_markup()
    await state.finish()
