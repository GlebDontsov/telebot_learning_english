from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram.utils.keyboard import ReplyKeyboardBuilder

from lexicon.lexicon_ru import LEXICON_RU

button_en_ru: KeyboardButton = KeyboardButton(text=LEXICON_RU['en-ru'])
button_ru_en: KeyboardButton = KeyboardButton(text=LEXICON_RU['ru-en'])
button_new_word: KeyboardButton = KeyboardButton(text=LEXICON_RU['new_word'])

button_builder: ReplyKeyboardBuilder = ReplyKeyboardBuilder()
button_builder.row(button_ru_en, button_en_ru, button_new_word, width=2)

en_ru_word_button = button_builder.as_markup(resize_keyboard=True)

button_cancel: KeyboardButton = KeyboardButton(text=LEXICON_RU['cancel'])
cancel_button: ReplyKeyboardMarkup = ReplyKeyboardMarkup(
    keyboard=[[button_cancel]],
    resize_keyboard=True)


