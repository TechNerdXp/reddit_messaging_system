from reddit import send_message, send_reply, get_messages, reddit_posts, create_reddit_instance, is_authenticated
from ai import create_thread, add_message, get_thread_messages, run_assistant
import json
from project_db import (
    get_posts, insert_post, insert_user, insert_message, check_message_status, update_message_status, update_openai_thread_id, update_reddit_message_id, 
    update_reddit_reply_id, get_reddit_reply_id, message_exists, get_config, insert_assistant_message_id, insert_reddit_message_id, assistant_message_id_exists, reddit_message_id_exists
)

import time
from project_logger import logger

def process_posts():
    admin_subreddits = None
    with open('admin_subreddits.json', 'r') as f:
        admin_subreddits = loaded_admin_subreddits = json.load(f)      

    for admin, subreddits in admin_subreddits.items():
        print(admin)
        if not is_authenticated(admin)['success']:
            print(f'{admin} is not authenticated. Pls authenticate using UI')
            continue
        
        reddit = create_reddit_instance(admin)
        for subreddit_name, keywords in subreddits.items():
            print(subreddit_name)
            print(keywords)
            posts = reddit_posts(admin, subreddit_name, keywords)
            for post in posts:
                insert_post(post)
                insert_user(post['author'])
            
                   
        posts = get_posts(admin)

        if not posts:
            print('No there are no posts to running messaging on.')
        for post in posts:
            message_status = post['message_status']
            post_id = post['id']
            assistant_thread_id = post['openai_thread_id']
            print(post['title'])
            print(message_status)
            if message_status == 'thread_not_started':
                message = post['title'] + '\n\n' + post['text']
                thread_id = create_thread()
                add_message(message, thread_id)
                update_openai_thread_id(post_id, thread_id)
                run_assistant(thread_id)
                update_message_status(post_id, 'waiting_for_the_assistant')
            elif message_status == 'waiting_for_the_assistant':
                thread_messages = get_thread_messages(assistant_thread_id)
                for message in thread_messages.data:
                    message_body = message.content[0].text.value
                    if message.role == 'assistant':
                        subject = post['title']
                        if post['reddit_message_id'] == None:
                            reddit_message_id = send_message(post['author'], subject[:100], message_body, reddit)
                            update_reddit_message_id(post_id, reddit_message_id)
                        elif not assistant_message_id_exists(message.id):
                            message_to_reply = post['reddit_reply_id']
                            send_reply(message_to_reply, message_body, reddit)
                            insert_assistant_message_id(message.id)
                            update_message_status(post_id, 'waiting_for_the_user')
                            time.sleep(int(get_config('DELAY_BETWEEN_MESSAGES')))
            elif message_status == 'waiting_for_the_user':
                reddit_messages = get_messages(reddit)
                for message in reddit_messages:
                    if message['id'] == post['reddit_message_id']:
                        for reply in message['replies']:
                            reply_id = reply['id']
                            if not reddit_message_id_exists(reply_id):
                                add_message(reply['body'], assistant_thread_id)
                                insert_reddit_message_id(reply_id)
                                update_reddit_reply_id(post_id, reply_id)
                                update_message_status(post_id, 'waiting_for_the_assistant')
                        run_assistant(assistant_thread_id)

while True:
    try:
        process_posts()
    except Exception as e:
        print(str(e))
        logger.error(str(e))
    time.sleep(30)
