from aiogram import types
from aiogram.dispatcher import FSMContext

from .training_states_group import Training
from handlers.users.start import IsPrivateChat
import keyboards
from loader import dp


# @dp.message_handler(IsPrivateChat(), state=Training.children_count)
# async def save_children_count(message: types.Message, state: FSMContext):
#     try:
#         children_count = int(message.text)
#         await state.update_data(children_count=children_count)
#         await message.answer("Выберите подходящий для вас вариант", reply_markup=keyboards.breakfast_keyboard)
#         await Training.breakfast.set()
#
#     except Exception as ex:
#         await message.answer("Введите число!")
