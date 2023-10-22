import json
import requests
from bs4 import BeautifulSoup
from urllib.parse import quote
from ulauncher.api.client.EventListener import EventListener
from ulauncher.api.client.Extension import Extension
from ulauncher.api.shared.action.CopyToClipboardAction import CopyToClipboardAction
from ulauncher.api.shared.action.RenderResultListAction import RenderResultListAction
from ulauncher.api.shared.event import KeywordQueryEvent
from ulauncher.api.shared.item.ExtensionResultItem import ExtensionResultItem

class DictionaryExtension(Extension):

    def __init__(self):
        super(DictionaryExtension, self).__init__()
        self.subscribe(KeywordQueryEvent, KeywordQueryEventListener())

class KeywordQueryEventListener(EventListener):

    API_BASE_URL = "https://www.oxfordlearnersdictionaries.com/definition/english/"
    
    def on_event(self, event, extension):
        query = event.get_argument().strip()
        if not query:
            return RenderResultListAction([ExtensionResultItem(
                icon='images/icon.png',
                name='No input provided',
                on_enter=CopyToClipboardAction('')
            )])

        word_url = self.API_BASE_URL + quote(query.lower())
        response = requests.get(word_url)

        if response.status_code == 200:
            soup = BeautifulSoup(response.content, 'html.parser')
            meanings = soup.find_all(class_='def')
            if meanings:
                meaning_text = meanings[0].text.strip()
                items = [
                    ExtensionResultItem(
                        icon='images/icon.png',
                        name=f'{query.capitalize()}: {meaning_text}',
                        on_enter=CopyToClipboardAction(meaning_text)
                    )
                ]
                return RenderResultListAction(items)
            else:
                return RenderResultListAction([ExtensionResultItem(
                    icon='images/icon.png',
                    name=f'Meaning not found for "{query}"',
                    on_enter=CopyToClipboardAction('')
                )])
        else:
            return RenderResultListAction([ExtensionResultItem(
                icon='images/icon.png',
                name='Failed to fetch data',
                on_enter=CopyToClipboardAction('')
            )])

if __name__ == '__main__':
    DictionaryExtension().run()
