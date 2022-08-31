import datetime
import os

import pandas as pd
from aiogram import types
from aiogram.types import InputFile

from filters import IsAdmin
from loader import dp, db


def delete_file(date):
    current = os.getcwd()
    if os.path.isfile(f'{current}\\{date}.xlsx'):
        os.remove(f'{current}\\{date}.xlsx')


@dp.callback_query_handler(IsAdmin(), text="breakfast_info")
async def breakfast_info(call: types.CallbackQuery):
    await call.message.answer("Отправляю таблицу: ")

    users = await db.get_users_info()
    fullnames, phones, children_count, meat_count, vegan_count = [], [], [], [], []

    for user in users:
        fullnames.append(user["fio"])
        phones.append(user["phone"])
        children_count.append(user["children_count"])
        meat_count.append(user["meat_count"])
        vegan_count.append(user["vegan_count"])

    df = pd.DataFrame({"ФИО": fullnames, "Телефон": phones, "Кол-во детей": children_count, "Мясной завтрак": meat_count,
                       "Веган": vegan_count})
    date = datetime.date.today()
    df.to_excel(f'./{date}.xlsx')
    await call.message.answer_document(InputFile(f'{date}.xlsx'))
    delete_file(date)
