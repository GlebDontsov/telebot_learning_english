from aiogram.fsm.state import State, StatesGroup


class FSMFillTranslationEnToRu(StatesGroup):
    translation_en_ru = State()


class FSMFillTranslationRuToEn(StatesGroup):
    translation_ru_en = State()
