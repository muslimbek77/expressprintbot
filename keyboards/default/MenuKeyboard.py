from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

menu = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text="Bog'cha"),
            KeyboardButton(text="Maktab"),
        ],
    ],
    resize_keyboard=True,
)