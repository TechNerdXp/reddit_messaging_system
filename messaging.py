from reddit import send_message, send_reply, get_messages, reddit_posts, create_reddit_instance, is_authenticated
from ai import create_thread, add_message, get_thread_messages, run_assistant
from project_db import get_posts, insert_post, insert_user, insert_message, check_message_status, update_message_status, update_openai_thread_id, update_reddit_message_id, update_reddit_reply_id, get_reddit_reply_id, message_exists
import time
from project_logger import logger

while True:
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
            try:
                posts = reddit_posts(admin, subreddit_name, keywords)
                for post in posts:
                    insert_post(post)
                    insert_user(post['author'])
            except Exception as e:
                print(e)
                print(str(e))
                   
        posts = get_posts(admin)

        if not posts:
            print('No there are no posts to running messaging on.')
        for post in posts:
            message_status = post['message_status']
            post_id = post['id']
            assistant_thread_id = post['openai_thread_id']
            print(post_id)
            print(message_status)
            print(assistant_thread_id)
            if message_status == 'thread_not_started':
                message = post['title'] + ' ' + post['text']
                thread_id = create_thread()
                message_id = add_message(message, thread_id)
                insert_message(post_id, message, message_id, 'post')
                update_openai_thread_id(post_id, thread_id)
                run_assistant(thread_id)
                update_message_status(post_id, 'waiting_for_the_assistant')
                pass
            elif message_status == 'waiting_for_the_assistant':
                thread_messages = get_thread_messages(post['openai_thread_id'])
                for message in thread_messages.data:
                    message_body = message.content[0].text.value
                    if not message_exists(message.id) and message.role == 'assistant':
                        subject = post['title']
                        if post['reddit_message_id'] == None:
                            reddit_message_id = send_message(post['author'], subject[:100], message_body, reddit)
                            update_reddit_message_id(post_id, reddit_message_id)
                        else:
                            message_to_reply = get_reddit_reply_id(post_id)
                            reddit_message_id = send_reply(message_to_reply, message_body, reddit)
                        insert_message(post_id, message_body, message.id, 'assistant')
                        update_message_status(post_id, 'waiting_for_the_user')
                    time.sleep(200)
            elif message_status == 'waiting_for_the_user':
                print('yes')
                reddit_messages = get_messages(reddit)
                for message in reddit_messages:
                    print(message)
                    if message['id'] == post['reddit_message_id']:
                        print('yes2')
                        for reply in message['replies']:
                            print(reply)
                            reply_id = reply['id']
                            if not message_exists(reply_id):
                                print('yes3')
                                assistant_message_id = add_message(reply['body'], assistant_thread_id)
                                insert_message(post_id, reply['body'], message['id'], 'reddit_user_reply')
                                update_reddit_reply_id(post_id, reply_id)
                                run_assistant(assistant_thread_id)
                                update_message_status(post_id, 'waiting_for_the_assistant')
            time.sleep(5)
time.sleep(30)
