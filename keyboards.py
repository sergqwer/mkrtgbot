from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

keyboard = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text='Показать статистику')
        ],
        [
            KeyboardButton(text='Поменять ключ')
        ],
        [
            KeyboardButton(text='Посмотреть баланс')
        ]
    ],
    resize_keyboard=True
)
