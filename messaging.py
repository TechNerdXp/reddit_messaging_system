from reddit import send_message, get_messages
from ai import create_thread, add_message, get_thread_messages, run_assistant
from project_db import get_posts, insert_message, check_message_status, update_message_status, update_openai_thread_id, update_reddit_message_id, mark_message_replied
import time

# Get all posts
posts = get_posts()

for post in posts:
    message_status = post['message_status']
    post_id = post['id']
    if message_status == 'thread_not_started':
        message = post['title'] + ' ' + post['text']
        thread_id = create_thread()
        add_message(message, thread_id)
        # insert_message(post_id, message, message_id, source)
        update_openai_thread_id(post['id'], thread_id)
        run_assistant(thread_id)
        update_message_status(post['id'], 'waiting_for_the_assistant')
    elif message_status == 'waiting_for_the_assistant':
        
        pass
    elif message_status == 'waiting_for_the_user':
        pass

    
    
time.sleep(5)
