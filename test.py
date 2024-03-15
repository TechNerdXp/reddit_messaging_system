from reddit import send_message, send_reply, get_messages, reddit_posts, create_reddit_instance, is_authenticated
from ai import create_thread, add_message, get_thread_messages, run_assistant
from project_db import (
    get_posts, insert_post, insert_user, update_message_status, update_openai_thread_id, update_reddit_message_id, 
    update_reddit_reply_id, get_config, insert_assistant_message_id, insert_reddit_message_id, assistant_message_id_exists, reddit_message_id_exists,
    get_admins_and_subreddits
)

import time
from project_logger import logger

def process_posts():
    admin_subreddits = get_admins_and_subreddits()
    
    for row in admin_subreddits:
        admin = row['username']
        if not is_authenticated(admin)['success']:
            print(f'{admin} is not authenticated. Pls authenticate using UI')
            continue
        
        reddit = create_reddit_instance(admin)

        posts = get_posts(admin)

        if not posts:
            print('No there are no posts to running messaging on.')
        for post in posts:
            message_status = post['message_status']
            post_id = post['id']
            assistant_thread_id = post['openai_thread_id']
            post_title = post['title']
            print(f'Messaging status: {message_status}')
            if message_status == 'thread_not_started':
                # message = post_title + '\n\n' + post['text']
                # thread_id = create_thread()
                # add_message(message, thread_id)
                # update_openai_thread_id(post_id, thread_id)
                # run_assistant(thread_id)
                # update_message_status(post_id, 'waiting_for_the_assistant')
                # time.sleep(20)
                pass
            elif message_status == 'waiting_for_the_assistant':
                # thread_messages = get_thread_messages(assistant_thread_id)
                # for message in thread_messages.data:
                #     message_body = message.content[0].text.value
                #     if message.role == 'assistant':
                #         subject = post_title
                #         if post['reddit_message_id'] == None:
                #             reddit_message_id = send_message(post['author'], subject[:100], message_body, reddit)
                #             update_reddit_message_id(post_id, reddit_message_id)
                #         elif not assistant_message_id_exists(message.id):
                #             message_to_reply = post['reddit_reply_id']
                #             send_reply(message_to_reply, message_body, reddit)
                #             insert_assistant_message_id(message.id)
                #             update_message_status(post_id, 'waiting_for_the_user')
                #         time.sleep(int(get_config('DELAY_BETWEEN_MESSAGES')))
                pass
            elif message_status == 'waiting_for_the_user':
                print('____running for waiting_for_the_user____')
                reddit_messages = get_messages(reddit)
                for message in reddit_messages:
                    if message['id'] == post['reddit_message_id']:
                        print('reddit message found')
                        for reply in message['replies']:
                            reply_id = reply['id']
                            print(f'reply sender: {reply["sender"]}, post author: {post["author"]}')
                            print(reply['sender'] == post['author'])
                            if not reddit_message_id_exists(reply_id) and reply['sender'] == post['author']:
                                print('sending reply')
                                add_message(reply['body'], assistant_thread_id)
                                insert_reddit_message_id(reply_id)
                                update_reddit_reply_id(post_id, reply_id)
                                update_message_status(post_id, 'waiting_for_the_assistant')
                                time.sleep(20)
                        run_assistant(assistant_thread_id)

if __name__ == '__main__':
    while True:
        try:
            process_posts()
        except Exception as e:
            print(str(e))
            logger.error(str(e))
        time.sleep(1200)