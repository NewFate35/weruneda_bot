from aiogram.types import ReplyKeyboardMarkup, InlineKeyboardMarkup, InlineKeyboardButton

markup_main = ReplyKeyboardMarkup(resize_keyboard=True, selective=True)
markup_main.add("Субботняя тренировка и завтрак\nРегистрация/Отмена записи")
markup_main.add("6.08 20:30 забег с кофейней DUO")
markup_main.add("F.A.Q.")
markup_main.add("Оставить отзыв")

cancel_markup = ReplyKeyboardMarkup(resize_keyboard=True, selective=True)
cancel_markup.add("Отмена")

markup_main_admin = ReplyKeyboardMarkup(resize_keyboard=True, selective=True)
markup_main_admin.add("Субботняя тренировка и завтрак\nРегистрация/Отмена записи")
markup_main_admin.add("6.08 20:30 забег с кофейней DUO")
markup_main_admin.add("F.A.Q.")
markup_main_admin.add("Оставить отзыв")
markup_main_admin.add("Режим админа")

admin_keyboard = ReplyKeyboardMarkup(resize_keyboard=True, selective=True)
admin_keyboard.add("Открыть регистрацию")
admin_keyboard.add("Закрыть регистрацию")
admin_keyboard.add("Кол-во участников")
admin_keyboard.add("Кол-во участников с DUO")
admin_keyboard.add("Сделать объявление")
admin_keyboard.add("Режим обычного пользователя")

faq_keyboard = InlineKeyboardMarkup(row_width=1)
button1 = InlineKeyboardButton(text="О проекте WeRunEda", callback_data="question_1")
button2 = InlineKeyboardButton(text="Я буду с ребенком", callback_data="question_2")
button3 = InlineKeyboardButton(text="Место для парковки", callback_data="question_3")
button4 = InlineKeyboardButton(text="Оплата завтрака", callback_data="question_4")
faq_keyboard.add(button1, button2, button3, button4)

inline_answers = {
    1: """Это комьюнити, в рамках которого проводятся еженедельные пробежки с авторскими завтраками от шеф-поваров Екатеринбурга.
Мы организуем встречи и лектории, чтобы делиться новыми знаниями, практическим опытом, полезными знакомствами.
Мы дарим общение в кругу единомышленников, вдохновение и заряд энергии.""",
    2: """Мы рады вам и вашим детям.\nСовместное времяпрепровождение способствует началу настоящей дружбы между взрослыми и детьми.
    """,
    3: 'Все машины паркуйте 🚗  около входа в парк КАЗАКИ РАЗБОЙНИКИ.',
    4: """Оплата за завтрак принимается по номеру телефона 8-922-208-07-08 (Сбер/Тинькофф) 

❗️Оплата принимается с момента регистрации до 11:00 субботы.""",
    5: " "
}

rules_keyboard = InlineKeyboardMarkup(row_width=1)
button = InlineKeyboardButton(text="Показать правила", callback_data="question_5")
rules_keyboard.add(button)

breakfast_keyboard = InlineKeyboardMarkup(row_width=1)
button1 = InlineKeyboardButton(text="Без завтрака", callback_data="without_breakfast")
button2 = InlineKeyboardButton(text="С мясным завтраком", callback_data="meat_breakfast")
button3 = InlineKeyboardButton(text="Вегетарианский завтрак", callback_data="vegan_breakfast")
breakfast_keyboard.add(button1, button2, button3)

edit_keyboard = InlineKeyboardMarkup(row_width=1)
button1 = InlineKeyboardButton(text="Изменить", callback_data="edit")
button2 = InlineKeyboardButton(text="Отменить запись", callback_data="cancel")
edit_keyboard.add(button1, button2)

breakfast_info_keyboard = InlineKeyboardMarkup(row_width=1)
button1 = InlineKeyboardButton(text="Полная таблица", callback_data="breakfast_info")
breakfast_info_keyboard.add(button1)
