from aiogram import Router
from aiogram.filters import Command, CommandStart, Text
from aiogram.types import Message, FSInputFile, CallbackQuery, ReplyKeyboardRemove
from keyboards.keyboards import en_ru_word_button, cancel_button, buttons_list_sets, card_inline_buttons
from lexicon.lexicon_ru import LEXICON_RU
from services.services import get_words, get_word, get_word_translation, get_voice, get_sets, get_key_from_set, update_data
from states.states import FSMTranslationEnToRu, FSMTranslationRuToEn, FSMChooseSets
from aiogram.fsm.context import FSMContext
from bot import db

router: Router = Router()
words: dict = get_words()
sets: dict = get_sets()


@router.message(CommandStart())
async def process_start_command(message: Message, state: FSMContext):
    await state.clear()
    if not db.existsUser(message.from_user.id):
        db.addUser(message.from_user.id,
                   message.from_user.first_name,
                   message.from_user.last_name)
    await message.answer(text=LEXICON_RU['/start'], reply_markup=en_ru_word_button)


@router.message(Command(commands=['help']))
async def process_help_command(message: Message, state: FSMContext):
    await state.clear()
    await message.answer(text=LEXICON_RU['/help'], reply_markup=en_ru_word_button)


@router.message(Text(text=LEXICON_RU['new_word']))
@router.message(Command(commands=['newword']))
async def process_new_word(message: Message):
    word, translation = get_word(words)
    user_id = message.from_user.id
    await message.answer(text=f"{word} - {translation}", reply_markup=en_ru_word_button)
    get_voice(word, user_id)
    await message.answer_audio(audio=FSInputFile(path=f'voices/{user_id}.opus'))


@router.message(Text(text=LEXICON_RU['ru-en']))
@router.message(Command(commands=['fromrutoen']))
async def process_translate_ru_to_en(message: Message, state: FSMContext):
    await state.clear()
    await message.answer(text=f'{LEXICON_RU["ru_ans"]}', reply_markup=cancel_button)
    await state.set_state(FSMTranslationRuToEn.translation_ru_en)


@router.message(Text(text=LEXICON_RU['en-ru']))
@router.message(Command(commands=['fromentoru']))
async def process_translate_en_to_ru(message: Message, state: FSMContext):
    await state.clear()
    await message.answer(text=f'{LEXICON_RU["en_ans"]}', reply_markup=cancel_button)
    await state.set_state(FSMTranslationEnToRu.translation_en_ru)


@router.message(Text(text=LEXICON_RU['sets']))
@router.message(Command(commands=['chooseset']))
async def process_choose_set(message: Message, state: FSMContext):
    await state.clear()
    await message.answer(text=f'{LEXICON_RU["sets_ans"]}', reply_markup=buttons_list_sets)
    await state.set_state(FSMChooseSets.choose_set)


@router.message(Text(text=LEXICON_RU['cancel']))
@router.message(Command(commands=['menu']))
async def process_cancel(message: Message, state: FSMContext):
    await message.answer(text=f'{LEXICON_RU["menu_ans"]}', reply_markup=en_ru_word_button)
    await state.clear()


@router.message(FSMTranslationEnToRu.translation_en_ru)
async def process_translation_en_to_ru_sent(message: Message):
    user_id = message.from_user.id
    user_message = message.text
    await message.answer(text=f'{get_word_translation(user_message, "en", "ru")}')
    get_voice(user_message, user_id)
    await message.answer_audio(audio=FSInputFile(path=f'voices/{user_id}.opus'))


@router.message(FSMTranslationRuToEn.translation_ru_en)
async def process_translation_ru_to_en_sent(message: Message):
    user_id = message.from_user.id
    translation = get_word_translation(message.text, "ru", "en")
    await message.answer(text=f'{translation}')
    get_voice(translation, user_id)
    await message.answer_audio(audio=FSInputFile(path=f'voices/{user_id}.opus'))


@router.message(FSMChooseSets.choose_set)
async def process_translation_ru_to_en_sent(message: Message, state: FSMContext):
    if message.text in sets:
        set_of_words = sets[message.text].copy()
        word = get_key_from_set(set_of_words)
        await state.update_data(choose_set=[set_of_words, 0, len(set_of_words), 0, 0, word['card']])
        await message.answer(text='Здорова, начнем!😝', reply_markup=cancel_button)
        await message.answer(text=f"0/{len(set_of_words)}  🇬🇧 {word['card']}   -   🇷🇺 {word['card2']}",
                             reply_markup=card_inline_buttons)
    else:
        await message.answer(text=LEXICON_RU['no_set'])


@router.callback_query(Text(text=['unknow']))
@router.callback_query(Text(text=['know']))
async def process_button_check(callback: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    if data:
        set_words = data['choose_set'][0]
        if set_words:
            update_data(callback, data)
            word = get_key_from_set(set_words)
            data['choose_set'][5] = word['card']
            await callback.message.edit_text(
                text=f"{data['choose_set'][1]}/{data['choose_set'][2]}  🇬🇧 {word['card']}   -   🇷🇺 {word['card2']}",
                reply_markup=callback.message.reply_markup)
        else:
            await callback.message.edit_text(text=f"{LEXICON_RU['end_words']}\n\n"
                                                  f"Вы знаете слов: {data['choose_set'][3]}\n"
                                                  f"Вы не знаете слов: {data['choose_set'][4]}")
            await state.clear()
    else:
        await callback.message.answer(text=f"{LEXICON_RU['data_outdated']}")
        await callback.message.delete()


@router.callback_query(Text(text=['microphone']))
async def process_button_check(callback: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    user_id = callback.message.from_user.id
    if data:
        get_voice(data['choose_set'][5], user_id)
        await callback.message.answer_audio(audio=FSInputFile(path=f'voices/{user_id}.opus'))
    else:
        await callback.message.answer(text=f"{LEXICON_RU['data_outdated']}")
        await callback.message.delete()

