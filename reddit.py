import praw

from dotenv import load_dotenv
import os

load_dotenv()

reddit = praw.Reddit(
    client_id=os.getenv('REDDIT_CLIENT_ID'),
    client_secret=os.getenv('REDDIT_CLIENT_SECRET'),
    user_agent=os.getenv('REDDIT_USER_AGENT'),
)
    
def reddit_posts(subreddit_name, limit=10, postType='top'):

    subreddit = reddit.subreddit(subreddit_name)
    if postType == 'hot':
        posts = subreddit.hot(limit=limit)
    elif postType == 'new':
        posts = subreddit.new(limit=limit)
    elif postType == 'controversial':
        posts = subreddit.controversial(limit=limit)
    elif postType == 'rising':
        posts = subreddit.rising(limit=limit)
    else:
        posts = subreddit.top(limit=limit)
        
    posts_data = []
    for post in posts:
        posts_data.append({'id':post.id, 'title': post.title, 'text': post.selftext, 'html': post.selftext_html, 'author': post.author.name, 'subreddit': post.subreddit.display_name, 'post_url': post.url})
    return posts_data


def get_messages(reddit, username, limit=10):
    user = reddit.redditor(username)
    messages = []

    for message in user.inbox(limit=limit):
        messages.append({'id': message.id, 'subject': message.subject, 'body': message.body})

    return messages

def send_message(reddit, username, subject, body):
    user = reddit.redditor(username)
    user.message(subject, body)
