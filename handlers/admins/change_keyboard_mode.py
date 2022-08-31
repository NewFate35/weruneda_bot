from aiogram import types

from filters import IsAdmin, IsPrivateChat
import keyboards
from loader import dp


@dp.message_handler(IsAdmin(), IsPrivateChat(), text="Режим админа")
async def admin_mode(message: types.Message):
    await message.answer("Клавиатура админа активирована", reply_markup=keyboards.admin_keyboard)


@dp.message_handler(IsAdmin(), IsPrivateChat(), text="Режим обычного пользователя")
async def user_mode(message: types.Message):
    await message.answer("Клавиатура юзера активирована", reply_markup=keyboards.main_markup(message.from_user.id))
