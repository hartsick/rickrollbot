import requests
import json
import random
from twy_REST import Twy_REST
from botutils.ai import MarkovChain

def gen_tweet_from_url(url):
    '''Given a URL, assembles tweet of less than 140 chars that includes a message, 
    shortened url, and a trending hashtag.'''
    short_url = shorten_url(url)
    hashtag = pick_hashtag()

    print "short_url: {0} {1}".format(short_url, hashtag)

    text = generate_text_from_hashtag(len(short_url), hashtag)
    tweet = "{0} {1} {2}".format(text, short_url, hashtag)

    return tweet

def shorten_url(url):
    '''Accepts a to-be shortened URL, then returns a shortened URL using
    Google's URL Shortener API.

    In the context of this bot, this is both
    to obscure the source and prevent revealing previews of the URL in
    the bot's tweets.'''

    post_url = 'https://www.googleapis.com/urlshortener/v1/url'
    payload = {'longUrl': url}
    headers = {'content-type': 'application/json'}

    r = requests.post(post_url, data=json.dumps(payload), headers=headers)
    r_hash = r.json()

    print r_hash
    return r_hash['id']

def pick_hashtag():
    '''Picks a trending hash tag from select areas'''
    woeids = { 'nyc': 2459115, 'la': 2442047, 'usa': 23424977 }
    woeid = random.choice(woeids.values())

    print "WOEID: {0}".format(woeid)

    hashtags = Twy_REST().get_trends_from_place(woeid=woeid, hashtag_only=True)

    return random.choice(hashtags)

def generate_text_from_hashtag(url_length, hashtag):
    '''Uses Markov model to generate an eBooks-style response to tweets with a given
    hashtag'''

    max_length = 140 - (url_length + len(hashtag) + 2)

    corpus = pull_sample_tweets(hashtag)

    markov = MarkovChain()

    # train it and generate message, accept first tweet under max char length
    for sentence in corpus:
        markov.train_sentence(sentence.encode('utf-8'))

    while True:
        tweet_text = markov.generate_sentence()

        if len(tweet_text) < max_length:
            break

    return tweet_text

def pull_sample_tweets(hashtag):
    '''Given a hashtag, returns a list of sample texts from relevant tweets'''
    tweets = Twy_REST().search(q=hashtag)

    print "Retrieved tweets for {0}".format(hashtag)
    texts = []
    for status in tweets['statuses']:
        # ignore retweets
        if status['text'][:2] is not u'RT':
            texts.append(status['text'])

    return texts
