from aiogram.fsm.state import State, StatesGroup


class FSMTranslationEnToRu(StatesGroup):
    translation_en_ru = State()


class FSMTranslationRuToEn(StatesGroup):
    translation_ru_en = State()


class FSMChooseSets(StatesGroup):
    choose_set = State()
