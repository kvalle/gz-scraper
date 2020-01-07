#!/usr/bin/env python

from lxml import html
import requests


def setup_session():
    s = requests.Session() 
    s.get('https://gamezone.no/avdelinger/brettspill-nettbutikk')
    s.post('https://gamezone.no/WebPages/Extras/SessionStateApi.aspx?ajax=true&action=ChangeSort', data='"Nyheter"')
    return s


def get_games_for_page(session, page=1):
    url = 'https://gamezone.no/avdelinger/brettspill-nettbutikk'
    if page > 1:
        url += "?pageID=" + str(page)

    page = session.get(url)
    tree = html.fromstring(page.content)

    return tree.xpath('//*[@id="Header1Label"]/text()')


def get_games(number_of_pages):
    session = setup_session()
    games_per_page = [get_games_for_page(session, page=page) for page in range(1, number_of_pages+1)]
    return [game for games in games_per_page for game in games]


def normalize_word(word):
    word = word.lower()
    word = ''.join(char for char in word if char.isalnum())
    return word


def is_relevant(game_name, relevant_name):
    game_words = map(normalize_word, game_name.split())
    relevant_words = map(normalize_word, relevant_name.split())
    return all(map(lambda word: word in game_words, relevant_words))


def is_filtered(game_name, filter_word):
    game_words = map(normalize_word, game_name.split())
    return normalize_word(filter_word) in game_words

      
if __name__ == "__main__":

    relevant = ["Aeon's End", "Marvel Champions"]
    filters = ["expansion", "insert"]
    number_of_pages = 1

    games = get_games(number_of_pages)

    for filter_word in filters:
        games = [game for game in games if not is_filtered(game, filter_word)]

    matches = []    
    for relevant_name in relevant:
        matches += [game for game in games if is_relevant(game, relevant_name)]

    print("\n".join(matches))
