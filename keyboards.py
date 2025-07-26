from pyrogram.types import ReplyKeyboardMarkup, InlineKeyboardMarkup
import buttons

main_keyboard = ReplyKeyboardMarkup(
    keyboard=[
        [buttons.time_button, buttons.help_button],
        [buttons.settings_button, buttons.random_button],
    ],
    resize_keyboard=True

)

settings_keyboard = ReplyKeyboardMarkup(
    keyboard=[
        [buttons.back_button]
    ],
    resize_keyboard=True
)
