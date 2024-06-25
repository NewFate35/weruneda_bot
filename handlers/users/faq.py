from aiogram import types
from aiogram.types import InputFile, MediaGroup

import keyboards
from filters import IsPrivateChat
from loader import dp


@dp.message_handler(IsPrivateChat(), text="F.A.Q.")
async def faq(message: types.Message):
    await message.answer("Часто задаваемые вопросы:", reply_markup=keyboards.faq_keyboard)


@dp.callback_query_handler(text_contains='question_')
async def faq_answers(call: types.CallbackQuery):
    code = int(call.data[-1])
    answers = keyboards.inline_answers

    data = answers.get(code)
    text = data.get("text")
    photos = data.get("photos")

    if isinstance(text, str):
        await call.message.answer(text)
        if photos:
            if len(photos) > 1:
                media_group = MediaGroup()
                for photo in photos:
                    media_group.attach_document(InputFile(photo))
                await call.message.answer_media_group(media_group)
            else:
                await call.message.answer_photo(InputFile(photos[0]))
    else:
        for idx, txt in enumerate(text):
            await call.message.answer(txt)
            if idx + 1 <= len(photos):
                await call.message.answer_photo(InputFile(photos[idx]))
