from reddit import send_message, get_messages, reddit_posts, create_reddit_instance, is_authenticated
from ai import create_thread, add_message, get_thread_messages, run_assistant
from project_db import get_posts, insert_post, insert_user, insert_message, check_message_status, update_message_status, update_openai_thread_id, update_reddit_message_id, message_exists, mark_message_replied
import time
from project_logger import logger


admin_subreddits = {
    'TechNerdXp': {
        'Java': ['ai', 'machine learning'],
        'Python': ['ai', 'machine learning']
    },
    'Heydrianpay': {
        'AskMechanics': ['My car won\'t start', 'an issue with my car', 'my car is making a noise', 'transmission issue', 'knocking sound', 'crank no start'],
    },
    # 'Partsnetwork878': {
    #     'AskMechanics': ['My car won\'t start', 'an issue with my car', 'my car is making a noise', 'transmission issue', 'knocking sound', 'crank no start'],
    # },
    # 'hghgj67': {
    #     'AskMechanics': ['My car won\'t start', 'an issue with my car', 'my car is making a noise', 'transmission issue', 'knocking sound', 'crank no start'],
    # }
}

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
        if message_status == 'thread_not_started':
            message = post['title'] + ' ' + post['text']
            thread_id = create_thread()
            message_id = add_message(message, thread_id)
            insert_message(post_id, message, message_id, 'post')
            update_openai_thread_id(post_id, thread_id)
            run_assistant(thread_id)
            update_message_status(post_id, 'waiting_for_the_assistant')
        elif message_status == 'waiting_for_the_assistant':
            thread_messages = get_thread_messages(post['openai_thread_id'])
            for message in thread_messages.data:
                message_body = message.content[0].text.value
                logger.debug(f'message role: {message.role}')
                if not message_exists(message.id) and message.role == 'assistant':
                    subject = post['title']
                    reddit_message_id = send_message(post['author'], subject[:100], message_body, reddit)
                    insert_message(post_id, message_body, message.id, 'assistant')
                    if post['reddit_message_id'] == None:
                        update_reddit_message_id(post_id, reddit_message_id)
                    update_message_status(post_id, 'waiting_for_the_user')
                time.sleep(200)
        elif message_status == 'waiting_for_the_user':
            reddit_messages = get_messages(reddit)
            for message in reddit_messages:
                if message['sender'] == post['author']:
                    if not message_exists(message.id):
                        assistant_message_id = add_message(message, assistant_thread_id)
                        insert_message(post_id, message.body, message.id, 'reddit_user')
                        run_assistant(assistant_thread_id)
                        for reply in message['replies']:
                            if not message_exists(reply.id):
                                assistant_message_id = add_message(reply['body'], assistant_thread_id)
                                insert_message(post_id, reply['body'], reply.id, 'reddit_user_reply')
                                run_assistant(assistant_thread_id)
                update_message_status(post_id, 'waiting_for_the_assistant')
        time.sleep(5)
