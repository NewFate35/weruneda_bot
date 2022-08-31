from aiogram import types
from aiogram.dispatcher.filters import BoundFilter

from config import ADMINS


class IsAdmin(BoundFilter):
    """
    Фильтр.
    Проверяет, есть ли пользователь в списке администраторов
    """

    async def check(self, message: types.Message):
        res = False
        for admin in ADMINS:
            if message.from_user.id == int(admin):
                res = True
        return res


class IsPrivateChat(BoundFilter):

    async def check(self, message: types.Message):
        res = False
        if message.chat.type == "private":
            res = True
        return res
