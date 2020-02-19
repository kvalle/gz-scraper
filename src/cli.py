#!/usr/bin/env python

import dynamodb
import argparse
import lambda_function
import os
import sys

def print_backlog():
    print("Backlog:\n")

    for item in dynamodb.get_backlog():
        name = item["game_name"]
        print('- "{}"'.format(name), end = '')

        if isinstance(item["exclude_keywords"], list) and len(item["exclude_keywords"]) > 0:
            excludes = ", ".join(item["exclude_keywords"])
            print(' (excluded keywords: {})'.format(excludes), end='')

        print()

if __name__ == "__main__":

    if not 'GZ_SCRAPER_EMAIL_PASSWORD' in os.environ:
        print("You need to set the GZ_SCRAPER_EMAIL_PASSWORD env variable.")
        sys.exit(1)

    if not 'AWS_SECRET_ACCESS_KEY' in os.environ:
        print("Looks like you forgot AWS credentials…")
        sys.exit(1)

    parser = argparse.ArgumentParser(prog='gz-scaper')
    subparsers = parser.add_subparsers(dest="subcommand", metavar="subcomands", required=True)

    parser_scrape = subparsers.add_parser('scrape', help='trigger the scraper locally')
    parser_list = subparsers.add_parser('list', help='display backlog items')

    parser_add = subparsers.add_parser('upsert', help='insert/update a backlog item')
    parser_add.add_argument('name', help="name of item")
    parser_add.add_argument('--exclude',
        nargs='*',
        default=["insert", "expansion"],
        help="keywords to exclude (default: insert, expansion)")

    args = parser.parse_args()

    if args.subcommand == "scrape":
        print("Running scraper.")
        lambda_function.run_scraper()
    elif args.subcommand == "list":
        print_backlog()
    elif args.subcommand == "upsert":
        dynamodb.add_item(args.name, args.exclude)
        print("Item added.")
