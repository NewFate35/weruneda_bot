from aiogram import types
from aiogram.dispatcher import FSMContext

from filters import IsPrivateChat
from loader import dp
from .training_states_group import Training


@dp.message_handler(IsPrivateChat(), state=Training.fullname)
async def save_fullname(message: types.Message, state: FSMContext):
    await state.update_data(FIO=message.text)
    await message.answer("Введите свой телефон:")
    await Training.phone.set()
