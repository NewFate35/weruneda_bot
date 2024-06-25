import os

from aiogram.types import ReplyKeyboardMarkup, InlineKeyboardMarkup, InlineKeyboardButton, KeyboardButton

from handlers.users.check_admin import check_admin


def main_markup(user_id):
    markup_main = ReplyKeyboardMarkup(resize_keyboard=True, selective=True)
    if check_admin(user_id):
        markup_main.add("Субботняя тренировка и завтрак\nРегистрация/Отмена записи")
        # markup_main.add("26.11 18:00 Мафия в кофейне DUO")
        markup_main.add("F.A.Q.")
        markup_main.add("Оставить отзыв")
        markup_main.add("Режим админа")
    else:
        markup_main.add("Субботняя тренировка и завтрак\nРегистрация/Отмена записи")
        # markup_main.add("26.11 18:00 Мафия в кофейне DUO")
        markup_main.add("F.A.Q.")
        markup_main.add("Оставить отзыв")

    return markup_main


cancel_markup = ReplyKeyboardMarkup(resize_keyboard=True, selective=True)
cancel_markup.add("Отмена")

admin_keyboard = ReplyKeyboardMarkup(resize_keyboard=True, selective=True)
admin_keyboard.add("Открыть регистрацию")
admin_keyboard.add("Закрыть регистрацию")
admin_keyboard.add("Кол-во участников")
# admin_keyboard.add("Кол-во участников с DUO")
admin_keyboard.add("Сделать объявление")
admin_keyboard.add("Режим обычного пользователя")

faq_keyboard = InlineKeyboardMarkup(row_width=1)
button1 = InlineKeyboardButton(text="О проекте", callback_data="question_1")
button2 = InlineKeyboardButton(text="Я буду с ребенком", callback_data="question_2")
button3 = InlineKeyboardButton(text="Место для парковки", callback_data="question_3")
button4 = InlineKeyboardButton(text="Оплата", callback_data="question_4")
faq_keyboard.add(button1, button2, button3, button4)


def get_path(title: str):
    return os.path.join("images", title)


inline_answers = {
    1: {
        "text": (
            "Мы - сообщество, в рамках которого проводятся:"
            "\n   •	Еженедельные пробежки с авторскими завтраками от шеф-поваров Екатеринбурга"
            "\n   •	Еженедельные кофейные забеги по 2 раза в неделю"
            "\n   •	Авторские соревнования и контрольные забеги"
            "\n   •	Встречи и лектории, чтобы делиться новыми знаниями, практическим опытом, полезными знакомствами"
            "\n   •	Благотворительные и инклюзивные мероприятия"
            "\n   •	Выезды на спортивные соревнования"
            "\n   •	Презентации авторской формы и мерча"
            "\n\nМы дарим общение в кругу единомышленников, вдохновение и заряд энергии."
            "\nПодробнее про наши активности:"
        ),
        # "photos": [get_path("eco_1.png"), get_path("eco_2.png")],
        "photos": ["AgACAgIAAxkDAALawGZ6TIuqKzfe_5bWYRBnavq3sKPlAAKy2TEbRlPQSzxB6r51_-BhAQADAgADcwADNQQ",
                   "AgACAgIAAxkDAALawWZ6TI3FVzN42Q2von86d_iN5PMDAAKz2TEbRlPQS7chDF1wMguOAQADAgADcwADNQQ"],
        "doc": "BQACAgIAAxkDAALawmZ6TJDm9NxGxtHFuqWOGSFsyMc5AAItTgACRlPQS8ZRHMyHPhVrNQQ"
    },
    2: {
        "text": (
            "Мы рады нашим юным спортсменам! Самому юному нашему гостю всего несколько месяцев."
            "\nДети могут пробежаться вместе с родителями, проехаться на велосипеде, стать участниками групповой тренировки, подождать в теплом домике и помочь повару с приготовлением завтрака."
            "\nВсе локации: домик, беговой маршрут, поле – находятся рядом."
            "\nСовместное спортивное времяпрепровождение отличный пример здорового образа жизни."
        ),
        # "photos": [get_path("kid.png")],
        "photos": ["AgACAgIAAxkDAALalGZ6Qr735nczVQt6xmrddZOBIdzOAAKK2TEbRlPQS0-Fpkg1nIGnAQADAgADcwADNQQ"]
    },
    3: {
        "text": [
            ("Наша локация: база отдыха «Карасики», домик «Форт Боярд»"
             "\nКак добраться до места?"
             "\nМашины оставляйте на парковке у ж/д переезда:"
             "\n    •	координаты парковки: 56.845694, 60.686649"
             "\n    •	адрес для ориентации на местности: ул. Большой Шарташский каменный карьер, 8.")
            ,
            "Далее идем по основной дороге прямо, после веревочного парка по левой стороне будет домик «Форт Боярд» с огороженной территорией. В нем можно переодеться и оставить вещи на время пробежки."
            , "Вам сюда"
        ],
        # "photos": [get_path("park_1.png"), get_path("park_2.png")],
        "photos": ["AgACAgIAAxkDAALalWZ6QsHLnLIVHG-wPpj2RCEt7EJlAAKL2TEbRlPQS49_c65EBHytAQADAgADcwADNQQ",
                   "AgACAgIAAxkDAALalmZ6QsbsiQldAAG1JhS5uJqAyx_Z5QACjNkxG0ZT0EuecQpEo9LJOgEAAwIAA3MAAzUE"]
    },
    4: {
        "text": (
            "Стоимость завтрака + групповая тренировка – 400 руб."
            "\n    •	Оплата за завтрак принимается по номеру телефона +7-912-618-19-37 (Сбер / Тинькофф) "
            "\n    •	Оплата принимается с момента открытия регистрации до 9:00 субботы"
            "\nРегистрация на завтрак обязательна."
            "\n\nСтоимость пробежки + групповая тренировка (без завтрака) – 100 руб."
            "\n    •	Оплата за завтрак принимается по номеру телефона +7-912-618-19-37 (Сбер / Тинькофф) "
            "\n    •	Оплата принимается с момента открытия регистрации до 9:00 субботы"
            "\n\nУчастие в групповой тренировке без завтрака возможно без предварительной регистрации."
        )
    },
    5: {
        "text": "О сообществе:"
    }
}

rules_keyboard = InlineKeyboardMarkup(row_width=1)
button = InlineKeyboardButton(text="Показать правила", callback_data="question_1")
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

phone_kb = ReplyKeyboardMarkup(resize_keyboard=True, selective=True)
phone_kb.add(KeyboardButton(text="Отправить 📞", request_contact=True))
