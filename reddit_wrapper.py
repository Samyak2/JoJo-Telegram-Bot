import os
from random import randint
import praw
from dotenv import load_dotenv
load_dotenv()

client_id = os.environ.get("CLIENT_ID")
client_secret = os.environ.get("CLIENT_SERVER")
user_agent = os.environ.get("USER_AGENT")

reddit = praw.Reddit(client_id=client_id,
                     client_secret=client_secret,
                     user_agent=user_agent)
subreddit = reddit.subreddit('shitpostcrusaders')

reddit_url = "https://www.reddit.com"

def return_post():
    post = subreddit.random().permalink

    return reddit_url + post

if __name__ == "__main__":
    print(return_post())
