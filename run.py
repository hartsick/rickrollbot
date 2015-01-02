from twython import Twython
from datetime import datetime
import time

def run_bot():

    '''Run tweets four-ish times daily during work hours'''
    while True:

        current_hour = datetime.now().hour
        if current_hour >= 7 and current_hour <= 19:
            try:
                twitter = Tweeter(Twython)
                tweet = WinterscapeGenerator().generate_tweet()
                twitter.tweet(tweet)

            except Exception as e:
                logging.exception(e)
            else:
                # tweet again in three hours
                time.sleep(10800)

        else:
            # check again in an hour
            time.sleep(3600)

def change_name():
    ''' Periodically change name, so the humans don't catch on'''
    while True:

        # TODO: Change name every 3 days
        current_hour = datetime.now().hour
        if current_hour >= 7 and current_hour <= 19:
            try:
                twitter = Tweeter(Twython)
                tweet = WinterscapeGenerator().generate_tweet()
                twitter.tweet(tweet)

            except Exception as e:
                logging.exception(e)
            else:
                # tweet again in three hours
                time.sleep(10800)

        else:
            # check again in an hour
            time.sleep(3600)


if __name__ == "__main__":

    run_bot()
