import praw
from pprint import pprint

from dotenv import load_dotenv
import os

load_dotenv()

client_id = os.getenv('REDDIT_CLIENT_ID')
client_secret = os.getenv('REDDIT_CLIENT_SECRET')
user_agent = os.getenv('REDDIT_USER_AGENT')
redirect_uri = os.getenv('REDDIT_REDIRECT_URI')

reddit = praw.Reddit(
    client_id=os.getenv('REDDIT_CLIENT_ID'),
    client_secret=os.getenv('REDDIT_CLIENT_SECRET'),
    user_agent=os.getenv('REDDIT_USER_AGENT'),
)

def reddit_posts(subreddit_name, limit=10):

    subreddit = reddit.subreddit(subreddit_name)
    top_posts = subreddit.hot(limit=limit)

    for post in top_posts:
        pprint(f'@{post.author.name}')
        pprint(vars(post))

def send_message(reddit, username, subject, body):
    user = reddit.redditor(username)
    user.message(subject=subject, message=body)
    
if __name__ == '__main__':
    send_message(reddit, 'NadeemGorsi', 'test message', 'test message from developer to his own reddit account.')
    
