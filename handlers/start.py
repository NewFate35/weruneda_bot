import datetime
import logging
import os
from contextlib import suppress

import pandas as pd
from aiogram import types
from aiogram.dispatcher.filters import BoundFilter
from aiogram.dispatcher.filters.builtin import CommandStart, Command, CommandHelp
from aiogram.dispatcher.filters.state import StatesGroup, State
from aiogram.dispatcher import FSMContext
from aiogram.types import InputFile

import config
from config import ADMINS
from keyboards import markup_main, markup_main_admin, admin_keyboard, faq_keyboard, inline_answers, cancel_markup, \
    breakfast_keyboard, edit_keyboard, breakfast_info_keyboard, rules_keyboard
from loader import dp, db, bot


class IsAdmin(BoundFilter):
    key = "is_admin"

    async def check(self, message: types.Message):
        res = False
        for admin in config.ADMINS:
            if message.from_user.id == int(admin):
                res = True
        return res


class IsPrivateChat(BoundFilter):

    async def check(self, message: types.Message):
        res = False
        if message.chat.type == "private":
            res = True
        return res


def check(user_id):
    res = False
    for admin in config.ADMINS:
        if user_id == int(admin):
            res = True
    return res


class Training(StatesGroup):
    FIO = State()
    phone = State()
    children_count = State()
    breakfast = State()
    breakfast_count = State()
    obyavlenie = State()
    otziv = State()


@dp.message_handler(content_types=types.ContentType.NEW_CHAT_MEMBERS)
async def new_chat_member(message: types.Message):
    last_msg = await db.select_last_msg_id()

    text = f"Добро пожаловать в сообщество We|Run|Eda!\nНажми на @weruneda_bot и изучи правила сообщества!"

    if message['new_chat_member']['first_name']:
        text = f"Добро пожаловать, {message['new_chat_member']['first_name']}, " \
               f"в сообщество We|Run|Eda!\nНажми на @weruneda_bot и изучи правила сообщества!"
        logging.info(f"Вступил новый участник - {message['new_chat_member']['first_name']}")

    if len(last_msg) > 0:
        await bot.delete_message(chat_id=message.chat.id, message_id=last_msg[0]['message_id'])
    msg = await message.answer(text=text)

    await db.insert_last_message_id(msg.message_id)


@dp.message_handler(IsAdmin(), IsPrivateChat(), text="Отмена", state="*")
async def cancel(message: types.Message, state: FSMContext):
    await state.finish()
    await message.answer("Отменено!", reply_markup=markup_main_admin)


@dp.message_handler(IsPrivateChat(), text="Отмена", state="*")
async def cancel(message: types.Message, state: FSMContext):
    await state.finish()
    await message.answer("Отменено!", reply_markup=markup_main)


@dp.message_handler(IsAdmin(), IsPrivateChat(), CommandStart())
async def bot_start(message: types.Message):
    await db.add_user(message.from_user.id)
    await message.answer("Приветствую тебя, админ! Mr. Fox🦊 на связи!", reply_markup=markup_main_admin)
    await message.answer("Нажми на кнопку ниже и обязательно прочтите наши правила!", reply_markup=rules_keyboard)


@dp.message_handler(CommandStart(), IsPrivateChat())
async def bot_start(message: types.Message):
    await db.add_user(message.from_user.id)
    await message.answer("Приветствую тебя, друг! Mr. Fox🦊 на связи!", reply_markup=markup_main)
    await message.answer("Нажми на кнопку ниже и обязательно прочтите наши правила!", reply_markup=rules_keyboard)


@dp.message_handler(IsAdmin(), IsPrivateChat(), text="Сделать объявление")
async def make_obyavlenie(message: types.Message):
    await message.answer("Напиши текст для рассылки:", reply_markup=cancel_markup)
    await Training.obyavlenie.set()


@dp.message_handler(IsAdmin(), IsPrivateChat(), state=Training.obyavlenie)
async def save_obyavlenie(message: types.Message, state: FSMContext):
    users = await db.select_all_id_users()
    await state.finish()
    for user in users:
        await bot.send_message(user["telegram_id"], message.text)

    await message.answer("Отправлено!", reply_markup=markup_main_admin)


@dp.message_handler(CommandHelp(), IsPrivateChat())
async def bot_help(message: types.Message):
    text = ("Список команд: ",
            "/start - Старт",
            # "/help - Получить справку"
            )

    await message.answer("\n".join(text))


@dp.message_handler(IsAdmin(), IsPrivateChat(), text="Режим админа")
async def admin_mode(message: types.Message):
    await message.answer("Клавиатура админа активирована", reply_markup=admin_keyboard)


@dp.message_handler(IsAdmin(), IsPrivateChat(), text="Режим обычного пользователя")
async def user_mode(message: types.Message):
    await message.answer("Клавиатура юзера активирована", reply_markup=markup_main_admin)


@dp.message_handler(IsPrivateChat(), text="F.A.Q.")
async def faq(message: types.Message):
    await message.answer("Часто задаваемые вопросы:", reply_markup=faq_keyboard)


@dp.callback_query_handler(text_contains='question_')
async def faq_answers(call: types.CallbackQuery):
    if call.data and call.data.startswith("question_"):
        code = call.data[-1:]
        if code.isdigit():
            code = int(code)
        for k, v in inline_answers.items():
            if k == code:
                if code == 3:
                    await bot.send_photo(call.from_user.id, caption=v, photo=InputFile('парковка.png'))
                elif code == 5:
                    await bot.send_document(call.from_user.id,
                                            document=InputFile(f"Правила_сообщества.pdf"),
                                            caption="Правила корпоративной культуры сообщества We|Run|Eda")
                else:
                    await bot.send_message(call.from_user.id, text=v)
        else:
            await bot.answer_callback_query(call.id)


@dp.message_handler(IsAdmin(), IsPrivateChat(), text="Открыть регистрацию")
async def open_reg(message: types.Message):
    await db.open_reg()
    await message.answer("Регистрация открыта!")


@dp.message_handler(IsAdmin(), IsPrivateChat(), text="Закрыть регистрацию")
async def close_reg(message: types.Message):
    await db.close_reg()
    await message.answer("Регистрация закрыта!")


@dp.message_handler(IsPrivateChat(), text="Оставить отзыв")
async def otziv(message: types.Message):
    await message.answer("Напишите свой отзыв:", reply_markup=cancel_markup)
    await Training.otziv.set()


@dp.message_handler(IsPrivateChat(), state=Training.otziv)
async def otziv(message: types.Message, state: FSMContext):
    if message.from_user.username:
        username = message.from_user.username
    elif message.from_user.full_name:
        username = message.from_user.full_name
    else:
        username = message.from_user.id
    msg = message.text
    text = f"Отзыв от @{username}\nТекст:\n{msg}"
    for admin in ADMINS:
        await bot.send_message(chat_id=admin, text=text)

    await state.finish()
    if check(message.from_user.id):
        await message.answer("Отзыв успешно отправлен, спасибо вам за обратную связь!", reply_markup=markup_main_admin)
    else:
        await message.answer("Отзыв успешно отправлен, спасибо вам за обратную связь!", reply_markup=markup_main)


@dp.message_handler(IsPrivateChat(), text="Субботняя тренировка и завтрак\nРегистрация/Отмена записи")
async def training(message: types.Message):
    check = await db.check_user(message.from_user.id)
    res = await db.check_reg_status()
    if check is not None:
        if check['meat_count'] > 0:
            text = f"Вы уже зарегистрированы!\nФИО: {check['fio']}\nТелефон: {check['phone']}\nДетей: " \
                   f"{check['children_count']}\nКол-во порций завтрака: {check['meat_count']}"
        elif check['vegan_count'] > 0:
            text = f"Вы уже зарегистрированы!\nФИО: {check['fio']}\nТелефон: {check['phone']}\nДетей: " \
                   f"{check['children_count']}\nКол-во порций завтрака: {check['vegan_count']}"
        else:
            text = f"Вы уже зарегистрированы!\nФИО: {check['fio']}\nТелефон: {check['phone']}\nДетей: " \
                   f"{check['children_count']}\nБез завтрака!"

        await message.answer(text=text, reply_markup=edit_keyboard)
    else:
        if res['status']:
            await message.answer("Введите своё ФИО:", reply_markup=cancel_markup)
            await Training.FIO.set()
        else:
            await message.answer("Регистрация закрыта!")


@dp.callback_query_handler(text="edit")
async def edit(call: types.CallbackQuery):
    res = await db.check_reg_status()
    if res['status']:
        await bot.send_message(call.from_user.id, "Введите своё ФИО:", reply_markup=cancel_markup)
        await Training.FIO.set()
    else:
        await bot.send_message(call.from_user.id, "Регистрация уже закрыта! Изменить информацию нельзя")


@dp.callback_query_handler(text="cancel")
async def cancel(call: types.CallbackQuery):
    res = await db.check_reg_status()
    if res['status']:
        if check(call.from_user.id):
            await db.delete_user(call.from_user.id)
            await bot.send_message(call.from_user.id, "Запись отменена :(", reply_markup=markup_main_admin)
        else:
            await db.delete_user(call.from_user.id)
            await bot.send_message(call.from_user.id, "Запись отменена :(", reply_markup=markup_main)
    else:
        await bot.send_message(call.from_user.id, "Регистрация уже закрыта! Изменить информацию нельзя")


@dp.message_handler(IsAdmin(), IsPrivateChat(), text="Кол-во участников")
async def count(message: types.Message, state: FSMContext):
    count = await db.count()
    children_count = await db.children_count()
    meat_count = await db.meat_count()
    vegan_count = await db.vegan_count()
    await message.answer(
        f"Всего участников: {count}\nДетей: {children_count}\nМясных завтраков: {meat_count}\nВеганов: {vegan_count}",
        reply_markup=breakfast_info_keyboard)


@dp.message_handler(IsAdmin(), IsPrivateChat(), commands='delete_all')
async def delete_all(message: types.Message, state: FSMContext):
    await db.delete_all()
    await message.answer("Таблица очищена!")


@dp.message_handler(IsPrivateChat(), state=Training.FIO)
async def save_fio(message: types.Message, state: FSMContext):
    await state.update_data(FIO=message.text)
    await message.answer("Введите свой телефон:")
    await Training.phone.set()


@dp.message_handler(IsPrivateChat(), state=Training.phone)
async def save_phone(message: types.Message, state: FSMContext):
    await state.update_data(phone=message.text)
    await message.answer("Вы будете с детьми? Если да, то отправьте их кол-во, иначе - 0")
    await Training.children_count.set()


@dp.message_handler(IsPrivateChat(), state=Training.children_count)
async def save_children_count(message: types.Message, state: FSMContext):
    await state.update_data(children_count=message.text)
    await message.answer("Выберите подходящий для вас вариант", reply_markup=breakfast_keyboard)
    await Training.breakfast.set()


@dp.callback_query_handler(text="without_breakfast", state=Training.breakfast)
async def without_breakfast(call: types.CallbackQuery, state: FSMContext):
    reg_data = await state.get_data()
    user_id = call.from_user.id
    FIO = reg_data['FIO']
    phone = reg_data['phone']
    children_count = reg_data['children_count']
    await db.add_user_training(user_id, FIO, phone, children_count, meat_count=0, vegan_count=0)

    if check(call.from_user.id):
        await bot.send_message(call.from_user.id,
                               text=f"ФИО: {FIO}\nТелефон: {phone}\nДетей: {children_count}\n"
                                    f"Успешная регистрация на тренировку без завтрака!",
                               reply_markup=markup_main_admin)
        await bot.send_message(call.message.from_user.id,
                               text="Не забудь про оплату!\nГрупповая тренировка - 100₽\nТренировка + завтрак - 400₽",
                               reply_markup=markup_main_admin)
    else:
        await bot.send_message(call.from_user.id,
                               text=f"ФИО: {FIO}\nТелефон: {phone}\nДетей: {children_count}\n"
                                    f"Успешная регистрация на тренировку без завтрака!",
                               reply_markup=markup_main)
        await bot.send_message(call.message.from_user.id,
                               text="Не забудь про оплату!\nГрупповая тренировка - 100₽\nТренировка + завтрак - 400₽",
                               reply_markup=markup_main)

    await state.finish()


@dp.callback_query_handler(text="meat_breakfast", state=Training.breakfast)
async def meat_breakfast(call: types.CallbackQuery, state: FSMContext):
    await state.update_data(breakfast="мясной")
    await bot.send_message(call.from_user.id, text="Кол-во порций завтрака:")
    await Training.breakfast_count.set()


@dp.callback_query_handler(text="vegan_breakfast", state=Training.breakfast)
async def vegan_breakfast(call: types.CallbackQuery, state: FSMContext):
    await state.update_data(breakfast="веган")
    await bot.send_message(call.from_user.id, text="Кол-во порций завтрака:")
    await Training.breakfast_count.set()


@dp.message_handler(IsPrivateChat(), state=Training.breakfast_count)
async def save_breakfast_count(message: types.Message, state: FSMContext):
    await state.update_data(breakfast_count=int(message.text))
    reg_data = await state.get_data()
    user_id = message.from_user.id
    FIO = reg_data['FIO']
    phone = reg_data['phone']
    children_count = reg_data['children_count']
    breakfast = reg_data['breakfast']
    breakfast_count = reg_data['breakfast_count']
    if breakfast == 'мясной':
        await db.add_user_training(user_id, FIO, phone, children_count, meat_count=breakfast_count, vegan_count=0)
    else:
        await db.add_user_training(user_id, FIO, phone, children_count, meat_count=0, vegan_count=breakfast_count)

    if check(message.from_user.id):
        await message.answer(
            text=f"ФИО: {FIO}\nТелефон: {phone}\nДетей: {children_count}\nКол-во порций завтрака: {breakfast_count}\n"
                 f"Успешная регистрация на тренировку и {breakfast} завтрак!",
            reply_markup=markup_main_admin)
        await message.answer(text="Не забудь про оплату!\nГрупповая тренировка - 100₽\nТренировка + завтрак - 400₽",
                             reply_markup=markup_main_admin)
    else:
        await message.answer(
            text=f"ФИО: {FIO}\nТелефон: {phone}\nДетей: {children_count}\nКол-во порций завтрака: {breakfast_count}\n"
                 f"Успешная регистрация на тренировку и {breakfast} завтрак!",
            reply_markup=markup_main)
        await message.answer(text="Не забудь про оплату!\nГрупповая тренировка - 100₽\nТренировка + завтрак - 400₽",
                             reply_markup=markup_main)
    await state.finish()


@dp.callback_query_handler(IsAdmin(), text="breakfast_info")
async def breakfast_info(call: types.CallbackQuery):
    await call.message.answer("Отправляю таблицу: ")

    users = await db.get_users_info()
    fio_s, phone_s, children_count, meat_count, vegan_count = [], [], [], [], []

    for user in users:
        fio_s.append(user["fio"])
        phone_s.append(user["phone"])
        children_count.append(user["children_count"])
        meat_count.append(user["meat_count"])
        vegan_count.append(user["vegan_count"])

    df = pd.DataFrame({"ФИО": fio_s, "Телефон": phone_s, "Кол-во детей": children_count, "Мясной завтрак": meat_count,
                       "Веган": vegan_count})
    date = datetime.date.today()
    df.to_excel(f'./{date}.xlsx')
    await call.message.answer_document(InputFile(f'{date}.xlsx'))
    delete_file(date)


def delete_file(date):
    current = os.getcwd()
    if os.path.isfile(f'{current}\\{date}.xlsx'):
        os.remove(f'{current}\\{date}.xlsx')
