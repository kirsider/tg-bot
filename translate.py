import requests
from langdetect import detect

api_key = "trnsl.1.1.20190426T200822Z.25adf2b80fed8c84.6b735695dd1a306802b0443d2a90a2e14bf84bf7"


def translate(text: str):
    current_lang = detect(text)
    lang = 'en'
    if is_latin(text) or current_lang == 'en':
        lang = 'ru'
    url = "https://translate.yandex.net/api/v1.5/tr.json/translate?key={0}&text={1}&lang={2}".format(api_key, text, lang)
    res = requests.post(url)
    return res.json()['text'][0]


def is_latin(text: str) -> bool:
    alphabet = 'qwertyuiopasdfghjklzxcvbnm '
    l_text = text.lower()
    count = 0
    for i in l_text:
        if i in alphabet:
            count += 1

    return float(count) > 0.8 * float(len(l_text))

