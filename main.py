#!/usr/bin/env python

import filtering
import scrape
import dynamodb

if __name__ == "__main__":

    backlog = dynamodb.get_backlog()
    new_games = scrape.get_games(number_of_pages=3)
    matching_items = filtering.filter_relevant_items(new_games, backlog)

    print("\n".join([item["game_name"] for item in matching_items]))
