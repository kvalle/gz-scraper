def filter_relevant_items(new_games, backlog):
    return [item for item in backlog if is_added_for_sale(item, new_games)]

def normalize_word(word):
    word = word.lower()
    word = ''.join(char for char in word if char.isalnum())
    return word


def is_relevant(game_name, relevant_name):
    game_words = map(normalize_word, game_name.split())
    relevant_words = map(normalize_word, relevant_name.split())
    return all(map(lambda word: word in game_words, relevant_words))


def is_excluded(game_name, filter_word):
    game_words = map(normalize_word, game_name.split())
    return normalize_word(filter_word) in game_words


def filter_out_excluded(games, excluded_words):
    for excluded_word in excluded_words:
        games = [game for game in games if not is_excluded(game, excluded_word)]

    return games


def is_added_for_sale(backlog_item, games):
    relevant = [game for game in games if is_relevant(game, backlog_item["game_name"])]
    relevant = filter_out_excluded(relevant, backlog_item["exclude_keywords"])

    return len(relevant) > 0
