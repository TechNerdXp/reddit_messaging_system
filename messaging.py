from reddit import send_message, get_messages
from ai import create_thread, add_message, get_thread_messages, run_assistant
from project_db import get_posts, insert_message, check_message_status, update_message_status, update_openai_thread_id, update_reddit_message_id, message_exists, mark_message_replied
import time

# Get all posts
posts = get_posts('TechNerdXp') # temp getting posts for technerd xp will get user from loop and nstansiate reddit class with ti and get posts for the user.

for post in posts:
    message_status = post['message_status']
    post_id = post['id']
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
            print("Message ID:", message.id)
            print("Thread ID:", message.thread_id)
            print("Message Content:", message.content[0].text.value)
            message_body = message.content[0].text.value
            if not message_exists(message.id):
                reddit_message_id = send_message(post['author'], post['title'], message_body)
                insert_message(message.id, message_body, message_id, 'assistant')
                if post['reddit_message_id'] == None:
                    update_reddit_message_id(post_id, reddit_message_id)
                update_message_status(post_id, 'waiting_for_the_user')
    elif message_status == 'waiting_for_the_user':
        # Get messages from Reddit
        reddit_messages = get_messages()
        # Check if the user has sent any message that the DB doesn't confirm
        for message in reddit_messages:
            if message['sender'] == post['author'] and not check_message_status(message['id']):
                # Add the user's message to the DB and the thread
                insert_message(post['id'], message['body'], message['id'], 'reddit')
                add_message(message['body'], post['openai_thread_id'])
                # Run the assistant on the thread
                run_assistant(post['openai_thread_id'])
                # Update the message status to 'waiting_for_the_assistant'
                update_message_status(post['id'], 'waiting_for_the_assistant')

    
    
time.sleep(5)
