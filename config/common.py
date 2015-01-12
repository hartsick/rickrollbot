import os

twitter_cred = [
    os.environ.get('MASTER_BOT_CONSUMER_KEY'),
    os.environ.get('MASTER_BOT_CONSUMER_SECRET'),
    os.environ.get('RICKROLL_ACCESS_TOKEN'),
    os.environ.get('RICKROLL_ACCESS_TOKEN_SECRET')
]

env_is_dev = True if os.environ.has_key('USER') else False
