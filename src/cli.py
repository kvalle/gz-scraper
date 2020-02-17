#!/usr/bin/env python

import lambda_function
import os
import sys

if __name__ == "__main__":

    if not 'GZ_SCRAPER_EMAIL_PASSWORD' in os.environ:
        print("You need to set the GZ_SCRAPER_EMAIL_PASSWORD env variable.")
        sys.exit(1)

    if not 'AWS_SECRET_ACCESS_KEY' in os.environ:
        print("Looks like you forgot AWS credentials…")
        sys.exit(1)

    lambda_function.run_scraper()
