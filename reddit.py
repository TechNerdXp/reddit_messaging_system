import praw
import os
import time
from dotenv import load_dotenv
import requests
from project_logger import logger
from project_db import insert_reddit_auth, get_reddit_auth, get_config, get_admins_list, insert_user_to_skip, user_exists_in_users_to_skip
from filters import filter_posts
from more_itertools  import peekable


load_dotenv()

def create_reddit_instance(username=None, refresh_token=None):
    
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
        admins = get_admins_list()
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
        url = 'https://www.reddit.com/api/v1/revoke_token'
        headers = {'User-Agent': os.getenv('REDDIT_USER_AGENT')}  
        data = {'token': token, 'token_type_hint': 'access_token'}
        response = requests.post(url, headers=headers, data=data, auth=(os.getenv('REDDIT_CLIENT_ID'), os.getenv('REDDIT_CLIENT_SECRET')))
        return {'success': True}
    except Exception as e:
        logger.error(f'Error in revoking token: {str(e)}')
        return {'success': False, 'error': str(e)}

def reddit_posts(admin, subreddit_name, keywords, reddit, max_pages=None, postType=None, limit=100):
    if max_pages is None:
        max_pages = int(get_config('REDDIT_MAX_PAGES_PER_SUBREDDIT'))
    if postType is None:
        postType = get_config('REDDIT_POST_TYPE')
    
    if reddit is None:
        reddit = create_reddit_instance()
        
    after = None
    all_posts_data = []
    for _ in range(max_pages):
        try:
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
        except Exception as e:
            logger.error(f'Error getting posts, {str(e)}')
            return []

        posts = peekable(posts)
        if not posts:
            logger.info('no more posts')
            break

        posts_data = []
        for post in posts:
            posts_data.append({'post_id':post.id, 'title': post.title, 'text': post.selftext, 'html': post.selftext_html, 'author': post.author.name if post.author else None, 'subreddit': post.subreddit.display_name, 'post_url': post.url, 'admin': admin})
        
        after = posts_data[-1]['post_id']
        all_posts_data.extend(posts_data)

        time.sleep(int(get_config('DELAY_IN_FETCHING_POSTS_IN_SECONDS')))
        
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
    try:
        reddit_messages = reddit.inbox.messages()
    except Exception as e:
        print(f'Error getting messages, {str(e)}')
        logger.error(f'Error getting messages, {str(e)}')
        return []
    for message in reddit_messages:
        replies = []
        for reply in message.replies:
            replies.append({'id': reply.id, 'body': reply.body, 'sender': str(reply.author), 'time': reply.created_utc})
        messages.append({'id': message.id, 'subject': message.subject, 'body': message.body, 'sender': str(message.author), 'time': message.created_utc, 'replies': replies})
    return messages

def send_message(recipient, subject, body, reddit):
    # recipient = 'HeydrianPay' # temp override for testing.
    if user_exists_in_users_to_skip(recipient):
        print(f"Skipping user {recipient} as they are in the users_to_skip list.")
        return
    try:
        user = reddit.redditor(recipient)
        user.message(subject=subject, message=body)
        for message in reddit.inbox.sent(limit=None):
            if message.dest == recipient and message.subject == subject and message.body == body:
                return message.id
    except Exception as e:
        print(f'Error sending message to {recipient}, {str(e)}')
        logger.error(f'Error sending message to {recipient}, {str(e)}')
        error_message = str(e)
        if 'NOT_WHITELISTED_BY_USER_MESSAGE' in error_message:
            insert_user_to_skip(recipient, 'Not whitelisted by user')
        elif 'USER_DOESNT_EXIST' in error_message:
            insert_user_to_skip(recipient, 'User does not exist')
        elif 'RATELIMIT' in error_message:
            wait_time = int(re.findall(r'\d+', error_message)[0])  # extract the number from the message
            if 'minute' in error_message:
                wait_time *= 60  # convert minutes to seconds
            time.sleep(wait_time)
        raise    
    
def send_reply(message_id, body, reddit):
    try:
        message = reddit.inbox.message(message_id)
        message.reply(body)
    except Exception as e:
        print(f'Error sending reply, {str(e)}')
        logger.error(f'Error sending reply, {str(e)}')
        raise
