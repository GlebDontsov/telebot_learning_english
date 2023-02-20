from aiogram import Router
from aiogram.filters import Command, CommandStart, Text
from aiogram.types import Message, FSInputFile
from keyboards.keyboards import en_ru_word_button, cancel_button
from lexicon.lexicon_ru import LEXICON_RU
from services.services import get_words, get_word, get_word_translation, get_voice
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
@router.message(Command(commands=['newword']))
async def process_new_word(message: Message):
    word, translation = get_word(words)
    user_id = message.from_user.id
    await message.answer(text=f"{word} - {translation}", reply_markup=en_ru_word_button)
    get_voice(word, user_id)
    await message.answer_audio(audio=FSInputFile(path=f'{user_id}.opus'))


@router.message(Text(text=LEXICON_RU['ru-en']))
@router.message(Command(commands=['fromrutoen']))
async def process_translate_ru_to_en(message: Message, state: FSMContext):
    await state.clear()
    await message.answer(text=f'{LEXICON_RU["ru_text"]}', reply_markup=cancel_button)
    await state.set_state(FSMFillTranslationRuToEn.translation_ru_en)


@router.message(Text(text=LEXICON_RU['en-ru']))
@router.message(Command(commands=['fromentoru']))
async def process_translate_en_to_ru(message: Message, state: FSMContext):
    await state.clear()
    await message.answer(text=f'{LEXICON_RU["en_text"]}', reply_markup=cancel_button)
    await state.set_state(FSMFillTranslationEnToRu.translation_en_ru)


@router.message(Text(text=LEXICON_RU['cancel']))
async def process_cancel(message: Message, state: FSMContext):
    await message.answer(text=f'{LEXICON_RU["menu_text"]}', reply_markup=en_ru_word_button)
    await state.clear()


@router.message(FSMFillTranslationEnToRu.translation_en_ru)
async def process_translation_en_to_ru_sent(message: Message):
    user_id = message.from_user.id
    user_message = message.text
    await message.answer(text=f'{get_word_translation(user_message, "en", "ru")}')
    get_voice(user_message, user_id)
    await message.answer_audio(audio=FSInputFile(path=f'{user_id}.opus'))


@router.message(FSMFillTranslationRuToEn.translation_ru_en)
async def process_translation_ru_to_en_sent(message: Message):
    user_id = message.from_user.id
    translation = get_word_translation(message.text, "ru", "en")
    await message.answer(text=f'{translation}')
    get_voice(translation, user_id)
    await message.answer_audio(audio=FSInputFile(path=f'{user_id}.opus'))
