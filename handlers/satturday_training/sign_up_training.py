from aiogram import types
from aiogram.dispatcher import FSMContext

from filters import IsPrivateChat
import keyboards
from loader import dp, db
from .training_states_group import Training


@dp.message_handler(IsPrivateChat(), text="Субботняя тренировка и завтрак\nРегистрация/Отмена записи")
async def training(message: types.Message, state: FSMContext):
    user_info = await db.check_user(message.from_user.id)
    reg_status = await db.check_reg_status()

    if user_info is not None:
        text = generate_text(user_info)
        await message.answer(text=text, reply_markup=keyboards.edit_keyboard)
    else:
        if reg_status['status']:
            check_user_data = await db.check_user_data(message.from_user.id)
            if check_user_data:
                await state.update_data(new_data=False)
                await state.update_data(FIO=check_user_data['full_name'])
                await state.update_data(phone=check_user_data['phone'])
                await message.answer("Выберите подходящий для вас вариант", reply_markup=keyboards.breakfast_keyboard)
                await Training.breakfast.set()
            else:
                await state.update_data(new_data=True)
                await message.answer("Введите своё ФИО:", reply_markup=keyboards.cancel_markup)
                await Training.fullname.set()
        else:
            await message.answer("Регистрация закрыта!")


def generate_text(user_info):
    fullname = user_info['fio']
    phone = user_info['phone']
    meat_count = user_info['meat_count']
    vegan_count = user_info['vegan_count']
    children_count = user_info['children_count']

    if meat_count > 0:
        text = f"Вы уже зарегистрированы! \nФИО: {fullname} \nТелефон: {phone} \nДетей: " \
               f"{children_count}\nКол-во порций завтрака: {meat_count}"
    elif vegan_count > 0:
        text = f"Вы уже зарегистрированы! \nФИО: {fullname} \nТелефон: {phone} \nДетей: " \
               f"{children_count}\nКол-во порций завтрака: {vegan_count}"
    else:
        text = f"Вы уже зарегистрированы! \nФИО: {fullname} \nТелефон: {phone} \nДетей:{children_count} \nБез завтрака!"
    return text
