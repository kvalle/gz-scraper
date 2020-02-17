import filtering
import scrape
import dynamodb
import mail

def lambda_handler(event, context):
    run_scraper()


def run_scraper():
    backlog = dynamodb.get_backlog()
    new_games = scrape.get_games(number_of_pages=3)

    if len(new_games) == 0:
        print("ERROR: Found no items while scraping. Something is probably wrong.")
    
    matching_items = filtering.filter_relevant_items(new_games, backlog)

    if len(matching_items) > 0:
        titles = [item["game_name"] for item in matching_items]

        print("Found {} relevant entries: {}.".format(len(matching_items), ", ".join(titles)))

        subject = "Nye greier hos Gamezone"
        body = "Gamezone har lagt ut noe nytt av interesse:\n\n"
        body += "\n".join(titles)

        mail.send(subject, body)

        print("Mail sent.")

        for item in matching_items:
            dynamodb.mark_as_found(item)

        print("Entries marked as found in DynamoDB.")

    else:
        print("No relevant entries found.")
