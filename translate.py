import requests

api_key = "trnsl.1.1.20190426T200822Z.25adf2b80fed8c84.6b735695dd1a306802b0443d2a90a2e14bf84bf7"


def translate(text, lang):
    url = "https://translate.yandex.net/api/v1.5/tr.json/translate?key={0}&text={1}&lang={2}".format(api_key, text, lang)
    res = requests.post(url)
    return res.json()['text'][0]

