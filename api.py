"""
Внешнее API: яндекс-переводчик и прочее
"""
from requests.sessions import Session

from private_settings import API_KEY_YANDEX

URL_YANDEX = 'https://translate.yandex.net/api/v1.5/tr.json/translate'
_session = Session()  # pylint: disable=invalid-name


# todo + cache
def translate_yandex(text: str, lang='en-ru') -> str:
    """
    Машинный перевод от яндекса
    :param text:
    :param lang:
    :return:
    """
    result = _session.request('POST', URL_YANDEX, data={
        'key': API_KEY_YANDEX,
        'text': text,
        'lang': lang,
    }).json()
    return result['text'][0]
