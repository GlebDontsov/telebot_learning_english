import random
import json
from googletrans import Translator


def get_words() -> dict:
    with open(f'words.json', 'r') as f:
        words = json.loads(f.read())
    return words


def get_word(dict_words: dict) -> tuple:
    key = random.choice(list(dict_words))
    word = dict_words[key]["word"]
    translation = dict_words[key]["translation"]
    return word, translation


def get_word_translation(text: str, src: str, dest: str) -> str:
    translator = Translator()
    result = translator.translate(text, src=src, dest=dest)
    return result.text

