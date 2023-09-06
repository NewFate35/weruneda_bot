from aiogram import types
from aiogram.dispatcher import FSMContext

from filters import IsPrivateChat
from loader import dp
from .training_states_group import Training
from keyboards import breakfast_keyboard


@dp.message_handler(IsPrivateChat(), state=Training.phone)
async def save_phone(message: types.Message, state: FSMContext):
    await state.update_data(phone=message.text)
    await message.answer("Выберите подходящий для вас вариант", reply_markup=breakfast_keyboard)
    await Training.breakfast.set()
    # await message.answer("Вы будете с детьми? Если да, то отправьте их кол-во, иначе - 0")
    # await Training.children_count.set()
