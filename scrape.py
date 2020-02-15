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
