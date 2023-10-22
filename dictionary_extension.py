import json
import logging
from ulauncher.api.client.Extension import Extension
from ulauncher.api.client.EventListener import EventListener
from ulauncher.api.shared.event import KeywordQueryEvent
from ulauncher.api.shared.item.ExtensionResultItem import ExtensionResultItem
from ulauncher.api.shared.action.RenderResultListAction import RenderResultListAction
import requests
from bs4 import BeautifulSoup

logger = logging.getLogger(__name__)


class DictionaryExtension(Extension):

    def __init__(self):
        super(DictionaryExtension, self).__init__()
        self.subscribe(KeywordQueryEvent, KeywordQueryEventListener())


class KeywordQueryEventListener(EventListener):

    def on_event(self, event, extension):
        query = event.get_argument() or ""
        meaning = get_word_meaning(query)
        item = ExtensionResultItem(icon='images/icon.png',
                                   name=meaning,
                                   on_enter=None)
        return RenderResultListAction([item])


def get_word_meaning(word):
    url = f"https://www.lexico.com/en/definition/{word}"
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')
    meaning_div = soup.find('span', class_='ind')
    if meaning_div:
        meaning = meaning_div.text.strip()
        return meaning
    else:
        return "Meaning not found."


if __name__ == '__main__':
    DictionaryExtension().run()
