from reddit import send_message, get_messages
from ai import create_thread, add_message, get_thread_messages
from project_db import get_posts, insert_message, check_message_status, update_message_status, update_openai_thread_id, update_reddit_message_id, mark_message_replied

import time

# Get all posts
posts = get_posts()

for post in posts:
    print(post['openai_thread_id'])
    continue
    # If the post doesn't have an OpenAI thread ID, create a new thread
    if not post['openai_thread_id']:
        thread_id = create_thread()
        update_openai_thread_id(post['id'], thread_id)
        add_message(post['title'] + ' ' + post['text'], thread_id)
    else:
        thread_id = post['openai_thread_id']

    # Get all messages in the thread
    thread_messages = get_thread_messages(thread_id)

    # If the last message is from the assistant and the message status is 'waiting_for_user'
    if thread_messages[-1]['source'] == 'openai' and post['message_status'] == 'waiting_for_user':
        # Send the assistant's message to the user
        send_message(post['author'], 'Re: ' + post['title'], thread_messages[-1]['message'])
        update_message_status(post['id'], 'waiting_for_assistant')

    # If the last message is from the user and the message status is 'waiting_for_assistant'
    elif thread_messages[-1]['source'] == 'reddit' and post['message_status'] == 'waiting_for_assistant':
        # Add the user's message to the thread
        add_message(thread_messages[-1]['message'], thread_id)
        update_message_status(post['id'], 'waiting_for_user')

    # Wait for a while before the next iteration
    time.sleep(5)
