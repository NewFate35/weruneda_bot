from aiogram import types
from aiogram.dispatcher import FSMContext

from handlers.satturday_training.training_states_group import Training
from loader import dp, bot


@dp.callback_query_handler(text="vegan_breakfast", state=Training.breakfast)
async def vegan_breakfast(call: types.CallbackQuery, state: FSMContext):
    await state.update_data(breakfast="веган")
    await bot.send_message(call.from_user.id, text="Кол-во порций завтрака:")
    await call.message.edit_reply_markup()
    await Training.breakfast_count.set()
