import random
import json
from googletrans import Translator
import gtts
import os


def get_sets() -> dict:
    dict_set: dict = dict()
    for filename in os.listdir("./sets"):
        with open(f'./sets/{filename}', 'r') as f:
            dict_set[filename[:-5]] = json.loads(f.read())
    return dict_set


def get_words() -> dict:
    with open(f'words.json', 'r') as f:
        words = json.loads(f.read())
    return words


def get_key_from_set(sets: dict) -> dict:
    data = sets[random.choice(list(sets))]
    del sets[random.choice(list(sets))]
    return data


def get_word(dict_words: dict) -> tuple:
    key = random.choice(list(dict_words))
    word = dict_words[key]["word"]
    translation = dict_words[key]["translation"]
    return word, translation


def get_word_translation(text: str, src: str, dest: str) -> str:
    translator = Translator()
    result = translator.translate(text, src=src, dest=dest)
    return result.text


def get_voice(text: str, filename: int) -> None:
    audio = gtts.gTTS(text)
    audio.save(f"voices/{str(filename)}.opus")


def update_data(callback, data) -> None:
    if callback.data == "know":
        data['choose_set'][3] += 1
    else:
        data['choose_set'][4] += 1
    data['choose_set'][1] += 1

