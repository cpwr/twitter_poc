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

# users = api.lookup_users(screen_name=["blabla"])
# user = users[0]
# print(user)
# user = api.get_user(user_id=user.id)
# print(user)
tweets = api.user_timeline(screen_name="blabla", count=20, exclude_replies=True, include_rts=True)
# tweets = api.user_timeline(screen_name="blabla", count=10, exclude_replies=True, truncated=False)
# print(tweets)
print(len(tweets))

for tweet in tweets:
    video_urls = []
    photo_urls = []

    if hasattr(tweet, "extended_entities"):
        for m in tweet.extended_entities.get("media", []):
            match media_type := m.get("type"):
                case "video":
                    video_urls = [v["url"] for v in m.get("video_info", {}).get("variants", [])]
                case "photo":
                    photo_urls = [v["url"] for v in m.get("video_info", {}).get("variants", [])]

    if is_quote_status := hasattr(tweet, "quoted_status"):
        quoted_author = tweet.quoted_status

    print({
        "id": tweet.id,
        "text": tweet.text,
        "link": f"https://twitter.com/i/web/status/{tweet.id}",
        "author_id": quoted_author.id if is_quote_status else tweet.user.id,
        "author_name": quoted_author.user.screen_name if is_quote_status else tweet.user.screen_name,
        "reply_to_id": tweet.in_reply_to_user_id or "",
        "reply_to_name": tweet.in_reply_to_screen_name or "",
        "owner_id": tweet.user.id,
        "owner_name": tweet.user.screen_name,
        "published_at": tweet.created_at.isoformat(),
        "images": photo_urls,
        "videos": video_urls,
        "forwards": tweet.retweet_count,
        # "replies": replies_count if replies else 0,
        "likes": tweet.favorite_count,
    })
