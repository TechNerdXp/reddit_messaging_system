import time
from project_logger import logger
from reddit import send_message, send_reply, get_messages, create_reddit_instance, is_authenticated
from ai import create_thread, add_message, get_thread_messages, run_assistant, check_run_status
from project_db import (
    get_posts, update_message_status, update_openai_thread_id, update_reddit_message_id, 
    get_config, insert_reddit_message_id, reddit_message_id_exists,
    get_admins_and_subreddits
)


def log_info(message):
    print(message)
    logger.info(message)

def process_posts():
    admin_subreddits = get_admins_and_subreddits()
    delay_between_messages = 3600 / int(get_config('REDDIT_MESSAGE_RATE_LIMIT_PER_HOUR'))
    replying = get_config('REPLYING')
    for row in admin_subreddits:
        admin = row['username']
        if not is_authenticated(admin)['success']:
            log_info(f'{admin} is not authenticated. Pls authenticate using UI')
            continue
        log_info(f'-------------------->>>>>>>>>>><<<<<<<<<<<-------------------')
        log_info(f'-------------------->>> Admin: {admin} <<<-------------------')
        log_info(f'-------------------->>>>>>>>>>><<<<<<<<<<<-------------------')

        reddit = create_reddit_instance(admin)   
                           
        posts = get_posts(admin)

        if not posts:
            log_info('No there are no posts to running messaging on.')
        for post in posts:
            try:
                message_status = post['message_status']
                post_id = post['id']
                assistant_thread_id = post['openai_thread_id']
                post_title = post['title']
                log_info(f'--->>> Running messaging for the post: {post_title}')
                log_info(f'Post conversation status {message_status} <<-----------------')
                if message_status == 'thread_not_started':
                    message = post_title + '\n\n' + post['text']
                    thread_id = create_thread()
                    add_message(message, thread_id)
                    run_id = run_assistant(thread_id)
                    log_info('Post sent to the assistant. ----------------->>>')
                    time.sleep(10)
                    status = check_run_status(thread_id, run_id)
                    while status != 'completed':
                        time.sleep(10)
                        print('Waiting for assistant to generate message...')
                        status = check_run_status(thread_id, run_id)
                        if status == 'expired' or status == 'failed':
                            logger.error('Assistant failed to generate message')
                            break
                    if status == 'completed':    
                        messages = get_thread_messages(thread_id)
                        message = messages.data[0]
                        message_body = message.content[0].text.value
                        subject = post_title[:100]
                        to = post['author']
                        reddit_message_id = send_message(to, subject, message_body, reddit)
                        update_openai_thread_id(post_id, thread_id)
                        update_reddit_message_id(post_id, reddit_message_id)
                        update_message_status(post_id, 'waiting_for_the_user')
                        log_info('Message sent to the user. ----------------->>>')
                        time.sleep(abs(delay_between_messages - 10))
                elif message_status == 'waiting_for_the_user' and replying == 1:
                    reddit_messages = get_messages(reddit)
                    for message in reddit_messages:
                        if message['id'] == post['reddit_message_id']:
                            for reply in message['replies']:
                                reply_id = reply['id']
                                if not reddit_message_id_exists(reply_id) and reply['sender'] == post['author']:
                                    add_message(reply['body'], assistant_thread_id)
                                    run_id = run_assistant(assistant_thread_id)
                                    log_info('Reply sent to the assistant. ----------------->>>')
                                    time.sleep(10)
                                    status = check_run_status(thread_id, run_id)
                                    while status != 'completed':
                                        time.sleep(10)
                                        print(f'status {status}')
                                        status = check_run_status(thread_id, run_id)
                                        if status == 'expired' or status == 'failed':
                                            logger.error('Assistant failed to generate reply')
                                            break
                                    if status == 'completed':
                                        messages = get_thread_messages(thread_id)
                                        message = messages.data[0]
                                        message_body = message.content[0].text.value
                                        send_reply(reply_id, message_body, reddit)
                                        time.sleep(abs(delay_between_messages - 10))
                                        insert_reddit_message_id(reply_id)
                                        update_message_status(post_id, 'waiting_for_the_user') # for updating updated_at field
                                        log_info('Reply sent to the user. ----------------->>>')
            except:
                pass
                

if __name__ == '__main__':
    while True:
        try:
            process_posts()
        except Exception as e:
            print(str(e))
            logger.error(str(e))
        time.sleep(1200)
