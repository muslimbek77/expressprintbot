from aiogram.types import ReplyKeyboardMarkup, KeyboardButton


menu = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text="🛍 Buyurtma berish"),
        ],
        [
        KeyboardButton(text="🛒 Savatcha"),
        KeyboardButton(text='Ko\'proq...'),
        KeyboardButton(text='🔎Qidirish'),
        ],
    ],
    resize_keyboard=True,
)

admin = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text="Reklama"),
            KeyboardButton(text="Mahsulot qo'shish"),
        ],
    ],
    resize_keyboard=True,
)

