from aiogram import Router
from aiogram.filters import Command, CommandStart, Text
from aiogram.types import Message
from keyboards.keyboards import en_ru_word_button, cancel_button
from lexicon.lexicon_ru import LEXICON_RU
from services.services import get_words, get_word, get_word_translation
from states.states import FSMFillTranslationEnToRu, FSMFillTranslationRuToEn
from aiogram.fsm.context import FSMContext

router: Router = Router()
words: dict = get_words()


@router.message(CommandStart())
async def process_start_command(message: Message):
    await message.answer(text=LEXICON_RU['/start'], reply_markup=en_ru_word_button)


@router.message(Command(commands=['help']))
async def process_help_command(message: Message):
    await message.answer(text=LEXICON_RU['/help'], reply_markup=en_ru_word_button)


@router.message(Text(text=LEXICON_RU['new_word']))
async def process_no_answer(message: Message):
    word, translation = get_word(words)
    await message.answer(text=f"{word} - {translation}", reply_markup=en_ru_word_button)


@router.message(Text(text=LEXICON_RU['ru-en']))
async def process_yes_answer(message: Message, state: FSMContext):
    await message.answer(text=f'{LEXICON_RU["ru_text"]}', reply_markup=cancel_button)
    await state.set_state(FSMFillTranslationRuToEn.translation_ru_en)


@router.message(Text(text=LEXICON_RU['en-ru']))
async def process_no_answer(message: Message, state: FSMContext):
    await message.answer(text=f'{LEXICON_RU["en_text"]}', reply_markup=cancel_button)
    await state.set_state(FSMFillTranslationEnToRu.translation_en_ru)


@router.message(Text(text=LEXICON_RU['cancel']))
async def process_no_answer(message: Message, state: FSMContext):
    await message.answer(text=f'{LEXICON_RU["menu_text"]}', reply_markup=en_ru_word_button)
    await state.clear()


@router.message(FSMFillTranslationEnToRu.translation_en_ru)
async def process_name_sent(message: Message, state: FSMContext):
    await message.answer(text=f'{get_word_translation(message.text, "en", "ru")}', reply_markup=en_ru_word_button)
    await state.clear()


@router.message(FSMFillTranslationRuToEn.translation_ru_en)
async def process_name_sent(message: Message, state: FSMContext):
    await message.answer(text=f'{get_word_translation(message.text, "ru", "en")}', reply_markup=en_ru_word_button)
    await state.clear()
