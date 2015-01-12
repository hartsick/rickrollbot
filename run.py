import logging
import time
from datetime import datetime

import nltk
from unipath import Path
nltk.data.path.append('./data/')

import bot.composer as composer
from bot.twy_REST import Twy_REST

def boostrap_nltk():
    # If we don't have NLTK data, grab it.
    nltkdata_exists = Path('./data/tokenizers/punkt/english.pickle')

    if not nltkdata_exists.exists():
        logging.info("Downloading NLTK Data")
        nltk.download('punkt', './data')

def run_bot():

    # '''Run tweets four-ish times daily during work hours'''
    while True:

        # current_hour = datetime.now().hour
        # if current_hour >= 7 and current_hour <= 19:
        try:
            # get shortened URL and craft tweet
            tweet = composer.gen_tweet_from_url("https://www.youtube.com/watch?v=dQw4w9WgXcQ")

            Twy_REST().update_status(tweet)

            # trend rate limit = 15 per 15 min
            time.sleep(60)

        except Exception as e:
            if e is Twy_REST.rate_exception:
                sleep_time = Twy_REST().get_seconds_until_reset()
                print "Rate limit hit. Resting for {0} seconds".format(sleep_time)
                time.sleep(sleep_time)
            else:
                time.sleep(60)

            logging.exception(e)
        else:
            # tweet again in ten min
            time.sleep(600)

# def change_name():
#     ''' Periodically change name, so the humans don't catch on'''
#     while True:

#         # TODO: Change name every 3 days
#         current_hour = datetime.now().hour
#         if current_hour >= 7 and current_hour <= 19:
#             try:
#                 twitter = Tweeter(Twython)
#                 tweet = WinterscapeGenerator().generate_tweet()
#                 twitter.tweet(tweet)

#             except Exception as e:
#                 logging.exception(e)
#             else:
#                 # tweet again in three hours
#                 time.sleep(10800)

#         else:
#             # check again in an hour
#             time.sleep(3600)


if __name__ == "__main__":

    boostrap_nltk()

    run_bot()
