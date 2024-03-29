from aiogram import types
from aiogram.dispatcher import FSMContext

from filters import IsPrivateChat
import keyboards
from loader import dp, db
from .training_states_group import Training


@dp.message_handler(IsPrivateChat(), state=Training.breakfast_count)
async def save_breakfast_count(message: types.Message, state: FSMContext):
    try:
        await state.update_data(breakfast_count=int(message.text))
        reg_data = await state.get_data()
        user_id = message.from_user.id
        fullname = reg_data['FIO']
        phone = reg_data['phone']
        breakfast = reg_data['breakfast']
        breakfast_count = reg_data['breakfast_count']

        if reg_data['new_data']:
            await db.add_or_update_user_data(message.from_user.id, fullname, phone)

        if breakfast == 'мясной':
            await db.add_user_training(user_id, fullname, phone, meat_count=breakfast_count,
                                       vegan_count=0)
        else:
            await db.add_user_training(user_id, fullname, phone, meat_count=0,
                                       vegan_count=breakfast_count)

        await message.answer(
            text=f"ФИО: {fullname}\nТелефон: {phone}\nКол-во порций завтрака: {breakfast_count}\n"
                 f"Успешная регистрация на тренировку и {breakfast} завтрак!",
            reply_markup=keyboards.edit_keyboard)
        await message.answer(text="➡️Оплата переводом по номеру: +7-912-618-19-37 (Сбербанк/Тинькофф)"
                                  "\nВ назначении платежа указывайте фамилию"
                                  "\n\nТренировка + завтрак - 400₽"
                                  "\nГрупповая тренировка - 100₽",
                             reply_markup=keyboards.main_markup(message.from_user.id))

        await state.finish()
    except Exception as ex:
        print(ex)
        await message.answer("Введите число!")

