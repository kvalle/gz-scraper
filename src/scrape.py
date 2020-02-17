import requests
from bs4 import BeautifulSoup

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
    html = page.content
    soup = BeautifulSoup(html, "html.parser")

    return [tag.string for tag in soup.find_all(id="Header1Label")]


def get_games(number_of_pages):
    session = setup_session()
    games_per_page = [get_games_for_page(session, page=page) for page in range(1, number_of_pages+1)]
    return [game for games in games_per_page for game in games]


if __name__ == "__main__":
    session = setup_session()
    games = get_games_for_page(session, page=2)
    print(games)
