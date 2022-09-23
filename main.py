import os

from tweepy import API
from tweepy import OAuth1UserHandler
from dotenv import load_dotenv

load_dotenv()

access_token = os.environ["access_token"]
access_token_secret = os.environ["access_token_secret"]
consumer_key = os.environ["consumer_key"]
consumer_secret_key = os.environ["consumer_secret_key"]

auth = OAuth1UserHandler(
   consumer_key=consumer_key, consumer_secret=consumer_secret_key,
   access_token=access_token, access_token_secret=access_token_secret,
)

api = API(auth, wait_on_rate_limit=True)

try:
    api.verify_credentials()
    print('Successful Authentication')
except Exception as err:
    print(f'Failed authentication: {err}')

# users = api.lookup_users(screen_name=["homepancakeua"])
# user = users[0]
# print(user)
# user = api.get_user(user_id=user.id)
# print(user)
tweets = api.user_timeline(screen_name="bmwant", count=10, exclude_replies=True)
# print(tweets)
print(len(tweets))

for tweet in tweets:
    print(tweet.id)
    print(tweet.text)
    print(tweet.created_at)
    print(tweet.in_reply_to_screen_name)
    print(tweet.author.id)
    print(tweet.user.id)
    print(tweet._json)
    break
