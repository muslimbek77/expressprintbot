from aiogram.types import ReplyKeyboardMarkup, KeyboardButton


menu = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text="๐ Buyurtma berish"),
        ],
        [
        KeyboardButton(text="๐ Savatcha"),
        KeyboardButton(text='Ko\'proq...'),
        KeyboardButton(text='๐Qidirish'),
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

