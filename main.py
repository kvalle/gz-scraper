#!/usr/bin/env python

import filtering
import scrape
import dynamodb
import mail

if __name__ == "__main__":

    backlog = dynamodb.get_backlog()
    new_games = scrape.get_games(number_of_pages=3)
    matching_items = filtering.filter_relevant_items(new_games, backlog)

    if len(matching_items) > 0:
        titles = [item["game_name"] for item in matching_items]

        print("Found {} relevant entries: {}.".format(len(matching_items), ", ".join(titles)))

        subject = "Nye greier hos Gamezone"
        body = "Gamezone har lagt ut noe nytt av interesse:\n\n"
        body += "\n".join(titles)

        mail.send(subject, body)

        print("Mail sent.")

    else:
        print("No relevant entries found.")
