from aiogram import types
from aiogram.dispatcher import FSMContext

from filters import IsPrivateChat
from loader import dp
from .training_states_group import Training
from keyboards import breakfast_keyboard


# content_types=types.ContentType.CONTACT,
@dp.message_handler(IsPrivateChat(), content_types=types.ContentType.CONTACT, state=Training.phone)
async def save_phone(message: types.Message, state: FSMContext):
    phone = message.contact.phone_number
    await state.update_data(phone=phone)
    await message.answer("Выберите подходящий для вас вариант", reply_markup=breakfast_keyboard)
    await Training.breakfast.set()

