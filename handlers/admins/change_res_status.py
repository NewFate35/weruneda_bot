from aiogram import types

from filters import IsAdmin, IsPrivateChat
from loader import dp, db


@dp.message_handler(IsAdmin(), IsPrivateChat(), text="Открыть регистрацию")
async def open_reg(message: types.Message):
    await db.open_reg()
    await message.answer("Регистрация открыта!")


@dp.message_handler(IsAdmin(), IsPrivateChat(), text="Закрыть регистрацию")
async def close_reg(message: types.Message):
    await db.close_reg()
    await message.answer("Регистрация закрыта!")
