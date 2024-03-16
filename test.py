from reddit import send_message, send_reply, get_messages, reddit_posts, create_reddit_instance, is_authenticated
from ai import create_thread, add_message, get_thread_messages, run_assistant
from project_db import (
    get_posts, insert_post, insert_user, update_message_status, update_openai_thread_id, update_reddit_message_id, 
    update_reddit_reply_id, get_config, insert_assistant_message_id, insert_reddit_message_id, assistant_message_id_exists, reddit_message_id_exists,
    get_admins_and_subreddits
)

import time
from project_logger import logger

def log_info(message):
    print(message)
    logger.info(message)

def process_posts():
    admin_subreddits = get_admins_and_subreddits()
    
    for row in admin_subreddits:
        admin = row['username']
        if not is_authenticated(admin)['success']:
            log_info(f'{admin} is not authenticated. Pls authenticate using UI')
            continue
        log_info(f'-------------------->>>>>>>>>>><<<<<<<<<<<-------------------')
        log_info(f'-------------------->>> Admin: {admin} <<<-------------------')
        log_info(f'-------------------->>>>>>>>>>><<<<<<<<<<<-------------------')

        reddit = create_reddit_instance(admin)

        subreddits = row['subreddits'].split()
        keywords = row['keywords'].split()
                           
        posts = get_posts(admin)

        if not posts:
            log_info('No there are no posts to running messaging on.')
        for post in posts:
            message_status = post['message_status']
            post_id = post['id']
            assistant_thread_id = post['openai_thread_id']
            post_title = post['title']
            if message_status == 'waiting_for_the_user':
                log_info(f'--->>> Running messaging for the post: {post_title}')
                log_info(f'Post conversation status {message_status} <<-----------------')
                reddit_messages = get_messages(reddit)
                for message in reddit_messages:
                    if message['id'] == post['reddit_message_id']:
                        print('reddit message was found')
                        for reply in message['replies']:
                            reply_id = reply['id']
                            print('sender:', reply['sender'])
                            print('reply id exists:', not reddit_message_id_exists(reply_id))
                            print('sender is hydrian:', reply['sender'] == 'Heydrianpay')
                            if not reddit_message_id_exists(reply_id) and reply['sender'] == 'Heydrianpay':
                                print('trying...')
                                try:
                                    add_message(reply['body'], assistant_thread_id)
                                    insert_reddit_message_id(reply_id)
                                    update_reddit_reply_id(post_id, reply_id)
                                    update_message_status(post_id, 'waiting_for_the_assistant')
                                    time.sleep(20)
                                    log_info('Reply sent to the assistant. ----------------->>>')
                                except Exception as e:
                                    print(str(e))
                                    pass
                        run_assistant(assistant_thread_id)

if __name__ == '__main__':
    while True:
        try:
            process_posts()
        except Exception as e:
            print(str(e))
            logger.error(str(e))
        time.sleep(1200)
