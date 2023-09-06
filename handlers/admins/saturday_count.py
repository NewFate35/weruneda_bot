from aiogram import types
from aiogram.dispatcher import FSMContext

from filters import IsAdmin, IsPrivateChat
import keyboards
from loader import dp, db


@dp.message_handler(IsAdmin(), IsPrivateChat(), text="Кол-во участников")
async def count(message: types.Message, state: FSMContext):
    users_count = await db.count()
    # children_count = await db.children_count()
    meat_count = await db.meat_count()
    vegan_count = await db.vegan_count()
    await message.answer(
        f"Всего участников: {users_count} \nМясных завтраков: {meat_count}"
        f"\nВеганов: {vegan_count}",
        reply_markup=keyboards.breakfast_info_keyboard)
