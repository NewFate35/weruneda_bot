from aiogram import types

from handlers.users.check_admin import check_admin
import keyboards
from loader import dp, db, bot


@dp.callback_query_handler(text="cancel")
async def cancel(call: types.CallbackQuery):
    res = await db.check_reg_status()
    if res['status']:
        await db.delete_user(call.from_user.id)
        await bot.send_message(call.from_user.id, "Запись отменена :(",
                               reply_markup=keyboards.main_markup(call.from_user.id))
        await call.message.edit_reply_markup()
    else:
        await bot.send_message(call.from_user.id, "Регистрация уже закрыта! Изменить информацию нельзя")
