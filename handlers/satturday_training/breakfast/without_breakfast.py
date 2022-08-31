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
    children_count = reg_data['children_count']

    if reg_data['new_data']:
        await db.add_or_update_user_data(call.from_user.id, fullname, phone)
    await db.add_user_training(user_id, fullname, phone, children_count, meat_count=0, vegan_count=0)

    await bot.send_message(call.from_user.id,
                           text=f"ФИО: {fullname}\nТелефон: {phone}\nДетей: {children_count}\n"
                                f"Успешная регистрация на тренировку без завтрака!",
                           reply_markup=keyboards.edit_keyboard)

    await bot.send_message(call.from_user.id,
                           text="Не забудь про оплату!\nГрупповая тренировка - 100₽\nТренировка + завтрак - 400₽",
                           reply_markup=keyboards.main_markup(call.from_user.id))
    await call.message.edit_reply_markup()
    await state.finish()
