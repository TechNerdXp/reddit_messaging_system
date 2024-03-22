from reddit import send_message, create_reddit_instance
from project_logger import logger
from project_db import user_exists_in_users_to_skip, insert_user_to_skip
import time
import re

reddit = create_reddit_instance('DiscussionAware113')

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
    
users = ['TechNerdXp', 'spammmmmmmmy', 'Otherwise_Voice3113']

for user in users:
    send_message(user, 'Test', 'Test', reddit)