import praw
import os
import time
from dotenv import load_dotenv
from flask import session
import requests
from project_logger import logger

load_dotenv()

def create_reddit_instance():
    """
    Create and return a Reddit instance with the refresh token from the session.
    """
    reddit = praw.Reddit(
        client_id=os.getenv('REDDIT_CLIENT_ID'),
        client_secret=os.getenv('REDDIT_CLIENT_SECRET'),
        user_agent=os.getenv('REDDIT_USER_AGENT'),
        redirect_uri=os.getenv('REDDIT_REDIRECT_URI'),
        refresh_token=session.get('REDDIT_REFRESH_TOKEN')
    )
    return reddit

def auth_url():
    reddit = create_reddit_instance()
    auth_url = reddit.auth.url(['identity', 'read', 'privatemessages'], 'axbycz', 'permanent')
    return {'authUrl': auth_url}

def authenticate(code):
    try:
        reddit = create_reddit_instance()
        refresh_token = reddit.auth.authorize(code)
        user = reddit.user.me()
        admins = os.getenv('ADMINS').split(',')
        if user.name not in admins:
            return {'success': 'false', 'message': 'User is not an admin'}
        session['REDDIT_REFRESH_TOKEN'] = refresh_token
        session['username'] = user.name
        return {'success': 'true', 'username': user.name}
    except Exception as e:
        logger.error(f'Error in getting refresh token: {str(e)}')
        return {'success': 'false'}

def is_authenticated():
    try:
        reddit = create_reddit_instance()
        isAuthenticated = reddit.user.me() is not None and session.get('username') is not None
    except Exception as e:
        logger.error(str(e))
        return {'error': str(e)}
    return {'isAuthenticated': isAuthenticated}

def revoke_token():
    try:
        token = session.get('REDDIT_REFRESH_TOKEN')
        url = "https://www.reddit.com/api/v1/revoke_token"
        headers = {"User-Agent": os.getenv('REDDIT_USER_AGENT')}  
        data = {"token": token, "token_type_hint": "access_token"}
        response = requests.post(url, headers=headers, data=data, auth=(os.getenv('REDDIT_CLIENT_ID'), os.getenv('REDDIT_CLIENT_SECRET')))
        session.clear()
        return response.status_code
    except Exception as e:
        logger.error(f'Error in revoking token: {str(e)}')
        return {'error': str(e)}


    
def reddit_posts(subreddit_name, max_pages=100, postType='top', limit=100):
    reddit = create_reddit_instance()
    after = None
    all_posts_data = []
    for _ in range(max_pages):
        subreddit = reddit.subreddit(subreddit_name)
        if postType == 'hot':
            posts = subreddit.hot(limit=limit, params={'after': after})
        elif postType == 'new':
            posts = subreddit.new(limit=limit, params={'after': after})
        elif postType == 'controversial':
            posts = subreddit.controversial(limit=limit, params={'after': after})
        elif postType == 'rising':
            posts = subreddit.rising(limit=limit, params={'after': after})
        else:
            posts = subreddit.top(limit=limit, params={'after': after})

        posts_data = []
        logger.debug(vars(posts))
        for post in posts:
            posts_data.append({'id':post.id, 'title': post.title, 'text': post.selftext, 'html': post.selftext_html, 'author': post.author.name, 'subreddit': post.subreddit.display_name, 'post_url': post.url})
        
        if not posts_data:
            break

        after = posts_data[-1]['id']
        all_posts_data.extend(posts_data)
        time.sleep(2)

    return all_posts_data



def get_messages():
    reddit = create_reddit_instance()
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

def send_message(username, subject, body):
    reddit = create_reddit_instance()
    user = reddit.redditor(username)
    user.message(subject=subject, message=body)
    
def reply_to_message_by_id(message_id):
    reddit = create_reddit_instance()
    message = reddit.inbox.message(message_id)
    message.reply("This is a reply to your message.")

