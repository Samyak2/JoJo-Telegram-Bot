import praw
import json
from random import randint

with open ('.secret-keys.json') as f:
    data = json.load(f)

client_id = data["client_id"]
client_secret = data["client_secret"]
user_agent = data["user_agent"]

reddit = praw.Reddit(client_id=client_id,
        client_secret=client_secret,
        user_agent=user_agent)
subreddit = reddit.subreddit('shitpostcrusaders')

top_100_posts = []

def return_post():
    for submission in subreddit.top(limit=100):
        top_100_posts.append(submission.url)

    post = randint(0,99)

    return top_100_posts[post]

if __name__ == "__main__":
    print(return_post())
