from aiogram import types
from aiogram.dispatcher import FSMContext

from filters import IsAdmin
from loader import dp, db


@dp.message_handler(IsAdmin(), text="Кол-во участников с DUO")
async def count(message: types.Message):
    users_count = await db.duo_count()
    await message.answer(f"Всего участников: {users_count}")
