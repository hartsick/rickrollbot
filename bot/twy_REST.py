import random
import logging
from twython import Twython
from twython.exceptions import TwythonRateLimitError
from config.common import twitter_cred, env_is_dev

class Twy_REST(object):
    '''If run on remote, completes action via Twython and prints output. /
        Otherwise, if run locally, only prints to terminal.'''

    rate_exception = TwythonRateLimitError

    def __init__(self):
        self.twitter = Twython(*twitter_cred)

    def update_status(self, text):
        params = {'status': text}
        if not env_is_dev:
            self.twitter.update_status(**params)
        print("SENT: Status: {0}".format(text))

    def send_dm(self, text, user):
        params = {'text': text, 'user_id': user.id, 'screen_name': user.username}
        if not env_is_dev:
            self.twitter.send_direct_message(**params)
        print("SENT: DM to {0} {1}: {2}".format(user.id, user.username, text))

    def follow_back(self, follow):
        if follow.sender_not_self():
            user = follow.sender()
            params = {'user_id': user.id, 'screen_name': user.username}
            if not env_is_dev:
                self.twitter.create_friendship(**params)
            print("SENT: Follow to {0} {1}".format(user.id, user.username))
        else:
            print "Cannot follow: Sender is self"

    def retweet(self, status):
        params = {'id': status.id_str}
        if not env_is_dev:
            self.twitter.retweet(**params)
        print("SENT: RT of {0}".format(status.id_str))

    def reply_to_status(self, status):
        print "reply received"
        if status.sender_not_self():
            status_type = status.check_type()
            print status_type
            if status_type:
                text = ""
                if status_type is 'resolution':
                    sentences = ["let's do this", "sweet.", "good luck with that", "interesting", "hm, okay!", "niiice"]
                    text = random.choice(sentences)
                elif status_type is 'help':
                    text = "send me your new year's resolution or prediction with 'in 2015' and I'll retweet it for all to see"
                elif status_type is 'complete':
                    text = "GOOD JOB!! :D"

                response = "@{0} {1}".format(status.sender().username, text)

                params = {'status': response, 'in_reply_to_status_id': status.id}
                print "SENT: Reply: {0}".format(response)
                if not env_is_dev:
                    self.twitter.update_status(**params)

    def get_trends_from_place(self, woeid=1, hashtag_only=False):
        params = { 'id': woeid }
        response = self.twitter.get_place_trends(**params)

        trends = []
        if response:
            trends = response[0]['trends']

        all_trends = []
        filtered_trends = []

        for trend in trends:
            # only keep non-promoted content
            if trend['promoted_content'] is None:
                # filter tragic hashes
                if "rip" in trend['name'].lower() or "r.i.p." in trend['name'].lower():
                    print "Death sensed. Skipping trend: {0}".format(trend['name'])
                # if hashtag_only selected, only include trends that start with hash tags
                elif hashtag_only:
                    if trend['name'][0] == u'#':
                        filtered_trends.append(trend['name'])
                    else:
                        pass
                else:
                    filtered_trends.append(trend['name'])

            all_trends.append((trend['name'], trend['promoted_content']))

        print "RECEIVED: All trends {0}".format(str(all_trends[1:-1]))
        print "RECEIVED: Filtered trends {0}".format(str(filtered_trends[1:-1]))

        return filtered_trends

    def get_seconds_until_reset(self):
        default = 60
        reset = self.twitter.get_lastfunction_header('x-rate-limit-reset', default_return_value=default)

        return reset

    def search(self, q=None, result_type=None, lang='en', count=50):
        '''Simple wrapper for Twython search'''
        results = self.twitter.search(q=q, result_type=result_type, lang=lang, count=count)

        return results
