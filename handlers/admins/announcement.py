from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import StatesGroup, State

from filters import IsAdmin, IsPrivateChat
import keyboards
from loader import dp, db, bot


class Announcement(StatesGroup):
    text = State()


@dp.message_handler(IsAdmin(), IsPrivateChat(), text="Сделать объявление")
async def make_announcement(message: types.Message):
    await message.answer("Напиши текст для рассылки:", reply_markup=keyboards.cancel_markup)
    await Announcement.text.set()


@dp.message_handler(IsAdmin(), IsPrivateChat(), state=Announcement.text)
async def save_announcement(message: types.Message, state: FSMContext):
    users = await db.select_all_id_users()
    await state.finish()
    for user in users:
        await bot.send_message(user["telegram_id"], message.text)

    await message.answer("Отправлено!", reply_markup=keyboards.main_markup(message.from_user.id))
