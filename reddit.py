import praw
import os
import time
from dotenv import load_dotenv
import requests
from project_logger import logger
from project_db import insert_reddit_auth, get_reddit_auth, get_config
from filters import filter_posts
from more_itertools  import peekable


load_dotenv()

def create_reddit_instance(username=None, refresh_token=None):
    """
    Creates a Reddit instance using the provided username and refresh token.
    """
    if refresh_token is None and username is not None:
        refresh_token = get_reddit_auth(username)
        
    reddit = praw.Reddit(
        client_id=os.getenv('REDDIT_CLIENT_ID'),
        client_secret=os.getenv('REDDIT_CLIENT_SECRET'),
        user_agent=os.getenv('REDDIT_USER_AGENT'),
        redirect_uri=os.getenv('REDDIT_REDIRECT_URI'),
        refresh_token=refresh_token
    )
    return reddit

def auth_url():
    try:
        reddit = create_reddit_instance()
        auth_url = reddit.auth.url(['identity', 'read', 'privatemessages'], 'axbycz', 'permanent')
        return {'authUrl': auth_url}
    except Exception as e:
        logger.error(f'Error in creating auth URL: {str(e)}')
        return {'success': False, 'authUrl': '#'}

def authenticate(code):
    try:
        reddit = create_reddit_instance()
        refresh_token = reddit.auth.authorize(code)
        user = reddit.user.me()
        admins = get_config('REDDIT_ADMINS').split(',')
        admin_username = user.name
        # logger.debug(admins)
        if admin_username not in admins:
            logger.info(f'{admin_username} is not an admin')
            return {'success': False, 'message': 'User is not an admin'}
        insert_reddit_auth(admin_username, refresh_token)
        return {'success': True, 'admin_username': admin_username, 'refresh_token': refresh_token}
    except Exception as e:
        logger.error(f'Error in authenticating: {str(e)}')
        return {'success': False, 'error': str(e)}

def is_authenticated(username):
    if username is None:
        return {'success': False, 'isAuthenticated': False, 'error': 'No username provided or session expired.'}
    try:
        reddit = create_reddit_instance(username)
        isAuthenticated = reddit.user.me() is not None
    except Exception as e:
        logger.error(f'Error in checking auth status: {str(e)}')
        return {'success': False, 'isAuthenticated': False, 'error': str(e)}
    return {'success': True, 'isAuthenticated': isAuthenticated, 'admin_username': username}

def revoke_auth(token):
    try:
        url = "https://www.reddit.com/api/v1/revoke_token"
        headers = {"User-Agent": os.getenv('REDDIT_USER_AGENT')}  
        data = {"token": token, "token_type_hint": "access_token"}
        response = requests.post(url, headers=headers, data=data, auth=(os.getenv('REDDIT_CLIENT_ID'), os.getenv('REDDIT_CLIENT_SECRET')))
        return {'success': True}
    except Exception as e:
        logger.error(f'Error in revoking token: {str(e)}')
        return {'success': False, 'error': str(e)}

def reddit_posts(admin, subreddit_name, keywords, max_pages=None, limit=None, postType=None):
    # is none max_pages get_config('REDDIT_MAX_PAGES_PER_SUBREDDIT')
    if max_pages is None:
        max_pages = int(get_config('REDDIT_MAX_PAGES_PER_SUBREDDIT'))
    if limit is None:
        limit = int(get_config('REDDIT_POSTS_PER_REQUEST'))
    if postType is None:
        postType = get_config('REDDIT_POST_TYPE')

    limit = 2 # temp override low limit for testing
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

        posts = peekable(posts)
        if not posts:
            logger.info('no more posts')
            break

        posts_data = []
        for post in posts:
            posts_data.append({'id':post.id, 'title': post.title, 'text': post.selftext, 'html': post.selftext_html, 'author': post.author.name if post.author else None, 'subreddit': post.subreddit.display_name, 'post_url': post.url, 'admin': admin})
        
        after = posts_data[-1]['id']
        all_posts_data.extend(posts_data)

        time.sleep(int(get_config('REDDIT_RATE_LIMIT')))
        
    all_posts_data = filter_posts(all_posts_data, keywords, False, 80)
    return all_posts_data

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

def send_message(recipient, subject, body, reddit):
    recipient = 'NadeemGorsi' # temporary override to avoid swarming users with test messages.
    user = reddit.redditor(recipient)
    user.message(subject=subject, message=body)
    for message in reddit.inbox.sent(limit=None):
        if message.dest == recipient and message.subject == subject and message.body == body:
            return message.id
    
def send_reply(message_id, body, reddit):
    message = reddit.inbox.message(message_id)
    message.reply(body)
