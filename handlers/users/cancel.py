from aiogram import types
from aiogram.dispatcher import FSMContext

from filters import IsPrivateChat
import keyboards
from loader import dp


@dp.message_handler(IsPrivateChat(), text="Отмена", state="*")
async def cancel(message: types.Message, state: FSMContext):
    await state.finish()
    await message.answer("Отменено!",
                         reply_markup=keyboards.main_markup(message.from_user.id))
