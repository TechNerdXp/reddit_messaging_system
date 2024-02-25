import praw

from dotenv import load_dotenv
import os

from project_db import insert_reddit_auth, get_reddit_auth
from project_logger import logger


load_dotenv()

reddit = praw.Reddit(
    client_id = os.getenv('REDDIT_CLIENT_ID'),
    client_secret = os.getenv('REDDIT_CLIENT_SECRET'),
    user_agent = os.getenv('REDDIT_USER_AGENT'),
    redirect_uri = os.getenv('REDDIT_REDIRECT_URI'),
    refresh_token=get_reddit_auth(os.getenv('REDDIT_USERNAME'))
)

def auth_url():
    auth_url = reddit.auth.url(['identity', 'read', 'privatemessages'], 'axbycz', 'permanent')
    return {'authUrl': auth_url}

def authenticate(code):
    try:
        refresh_token = reddit.auth.authorize(code)
    except Exception as e:
        logger.error(f'error in getting rfresh token{str(e)}')
        return {'success': 'false'}
    insert_reddit_auth(os.getenv('REDDIT_USERNAME'), refresh_token)
    return {'success': 'true'}

def is_authenticated():
    try:
        isAuthenticated = reddit.user.me() is not None
    except Exception as e:
        logger.error(str(e))
        return {'error': str(e)}
    return {'isAuthenticated': isAuthenticated}
    
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


def get_messages(reddit):
    messages = []
    # reddit.inbox.all()
    # reddit.inbox.unread()
    # # reddit.inbox.mark_read(items)
    # # reddit.inbox.mark_unread(items)
    # reddit.inbox.comment_replies()
    # reddit.inbox.message()
    # reddit.inbox.submission_replies()
    # reddit.inbox.mention()

    for message in reddit.inbox.messages():
        replies = []
        for reply in message.replies:
            replies.append({'id': reply.id, 'body': reply.body, 'sender': str(reply.author), 'time': reply.created_utc})
        messages.append({'id': message.id, 'subject': message.subject, 'body': message.body, 'sender': str(message.author), 'time': message.created_utc, 'replies': replies})
    return messages

def send_message(reddit, username, subject, body):
    user = reddit.redditor(username)
    user.message(subject=subject, message=body)
    
def reply_to_message_by_id(reddit, message_id):
    message = reddit.inbox.message(message_id)
    message.reply("This is a reply to your message.")

