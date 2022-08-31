from aiogram import types
from aiogram.types import InputFile

from filters import IsPrivateChat
import keyboards
from loader import dp, bot


@dp.message_handler(IsPrivateChat(), text="F.A.Q.")
async def faq(message: types.Message):
    await message.answer("Часто задаваемые вопросы:", reply_markup=keyboards.faq_keyboard)


@dp.callback_query_handler(text_contains='question_')
async def faq_answers(call: types.CallbackQuery):
    if call.data and call.data.startswith("question_"):
        code = call.data[-1:]
        if code.isdigit():
            code = int(code)
        for k, v in keyboards.inline_answers.items():
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
