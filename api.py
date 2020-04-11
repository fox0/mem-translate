from requests.sessions import Session

from private_settings import API_KEY_YANDEX

s = Session()


# todo + cache
def translate_yandex(text, lang='en-ru'):
    r = s.request('POST', 'https://translate.yandex.net/api/v1.5/tr.json/translate', data={
        'key': API_KEY_YANDEX,
        'text': text,
        'lang': lang,
    }).json()
    return r['text'][0]
