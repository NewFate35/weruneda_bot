from aiogram import types
from aiogram.dispatcher.filters.builtin import CommandStart

from filters import IsAdmin, IsPrivateChat
from handlers.users.check_admin import check_admin
import keyboards
from loader import dp, db


@dp.message_handler(IsPrivateChat(), CommandStart())
async def bot_start(message: types.Message):
    await db.add_user(message.from_user.id)
    name = 'админ' if check_admin(message.from_user.id) else 'друг'
    await message.answer(f"Приветствую тебя, {name}! Mr. Fox🦊 на связи!",
                         reply_markup=keyboards.main_markup(message.from_user.id))
    await message.answer("Нажми на кнопку ниже и обязательно прочтите наши правила!",
                         reply_markup=keyboards.rules_keyboard)


@dp.message_handler(IsAdmin(), IsPrivateChat(), commands='delete_all')
async def delete_all(message: types.Message):
    await db.delete_all_from_saturday()
    await message.answer("Таблица очищена!")
