import logging

from aiogram import types

from loader import dp, db, bot


@dp.message_handler(content_types=types.ContentType.NEW_CHAT_MEMBERS)
async def new_chat_member(message: types.Message):
    last_msg = await db.select_last_msg_id()

    text = f"Добро пожаловать в сообщество We|Run|Eda!\nНажми на @weruneda_bot и изучи правила сообщества!"

    if message['new_chat_member']['first_name']:
        text = f"Добро пожаловать, {message['new_chat_member']['first_name']}, " \
               f"в сообщество We|Run|Eda!\nНажми на @weruneda_bot и изучи правила сообщества!"
        logging.info(f"Вступил новый участник - {message['new_chat_member']['first_name']}")

    msg = await message.answer(text=text)
    if len(last_msg) > 0:
        try:
            await bot.delete_message(chat_id=message.chat.id, message_id=last_msg[0]['message_id'])
        except Exception:
            await drop_table_last_message()

    await db.insert_last_message_id(msg.message_id)


async def drop_table_last_message():
    await db.drop_table_last_mess()
    logging.info("Приветствие бота перезагружено!")
