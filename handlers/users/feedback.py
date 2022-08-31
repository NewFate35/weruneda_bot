from unittest.mock import call

from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import StatesGroup, State

from config import ADMINS
from filters import IsPrivateChat
from handlers.users.check_admin import check_admin
import keyboards
from loader import dp, bot


class Feedback(StatesGroup):
    text = State()


@dp.message_handler(IsPrivateChat(), text="Оставить отзыв")
async def make_feedback(message: types.Message):
    await message.answer("Напишите свой отзыв:", reply_markup=keyboards.cancel_markup)
    await Feedback.text.set()


@dp.message_handler(IsPrivateChat(), state=Feedback.text)
async def send_feedback(message: types.Message, state: FSMContext):
    if message.from_user.username:
        username = message.from_user.username
    elif message.from_user.full_name:
        username = message.from_user.full_name
    else:
        username = message.from_user.id
    msg = message.text
    text = f"Отзыв от @{username}\nТекст:\n{msg}"
    for admin in ADMINS:
        await bot.send_message(chat_id=admin, text=text)

    await state.finish()
    await message.answer("Отзыв успешно отправлен, спасибо вам за обратную связь!",
                         reply_markup=keyboards.main_markup(call.from_user.id))
