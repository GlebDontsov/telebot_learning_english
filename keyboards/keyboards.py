import os
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram.utils.keyboard import ReplyKeyboardBuilder, InlineKeyboardBuilder
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from lexicon.lexicon_ru import LEXICON_RU, LEXICON_INLINE_RU

button_en_ru: KeyboardButton = KeyboardButton(text=LEXICON_RU['en-ru'])
button_ru_en: KeyboardButton = KeyboardButton(text=LEXICON_RU['ru-en'])
button_list: KeyboardButton = KeyboardButton(text=LEXICON_RU['sets'])
button_new_word: KeyboardButton = KeyboardButton(text=LEXICON_RU['new_word'])
button_builder: ReplyKeyboardBuilder = ReplyKeyboardBuilder()
button_builder.row(button_ru_en, button_en_ru, button_list, button_new_word, width=2)
en_ru_word_button = button_builder.as_markup(resize_keyboard=True)

button_cancel: KeyboardButton = KeyboardButton(text=LEXICON_RU['cancel'])
cancel_button: ReplyKeyboardMarkup = ReplyKeyboardMarkup(
    keyboard=[[button_cancel]],
    resize_keyboard=True)

button_sets: list = [
    [KeyboardButton(text=f'{filename[:-5]}')] for filename in os.listdir("./sets")]
buttons_list_sets: ReplyKeyboardMarkup = ReplyKeyboardMarkup(
    keyboard=button_sets,
    resize_keyboard=True)

card_builder: InlineKeyboardBuilder = InlineKeyboardBuilder()
card_buttons: list = []
for button in LEXICON_INLINE_RU:
    card_buttons.append(InlineKeyboardButton(
        text=LEXICON_INLINE_RU[button],
        callback_data=button))
card_inline_buttons = card_builder.row(*card_buttons, width=2).as_markup()

