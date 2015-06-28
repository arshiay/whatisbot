import logging
import asyncio
import aiohttp
import os
from telebot import TeleBot

bot = TeleBot(os.environ["API_TOKEN"])

@asyncio.coroutine
def search_wiki(text, lang="en"):
    url = "https://{0}.wikipedia.org/w/api.php".format(lang)
    params = {
        'titles': text,
        'action': 'query',
        'exintro': '',
        'format': 'json', 
        'prop': 'extracts', 
        'explaintext': '',
        'redirects': ''
    }
    response = yield from bot.session.request('GET', url, params=params)
    assert response.status == 200
    return (yield from response.json())

@asyncio.coroutine
def wiki(message, match, lang):
    text = match.group(2)
    wiki = yield from search_wiki(text, lang)
    pages = wiki["query"]["pages"]
    for pid, page in pages.items():
        if pid == '-1':
            return (yield from bot.reply_to(message, "Not found :("))
        yield from bot.reply_to(message, page['extract'])


@bot.command(r"/?(whatis|what is|define|wiki) (.*)")
def wiki_en(message, match):
    return wiki(message, match, "en")

@bot.command(r"/?(что такое|что за|опредиление|вики) (.*)")
def wiki_ru(message, match):
    return wiki(message, match, "ru")

logging.basicConfig(level=logging.DEBUG)

loop = asyncio.get_event_loop()
loop.run_until_complete(bot.loop())