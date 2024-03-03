from reddit import send_message, get_messages
from ai import create_thread, add_message, get_thread_messages
from project_db import get_posts, insert_message, check_message_status, update_message_status, update_openai_thread_id, update_reddit_message_id, mark_message_replied

# get_messages(): This function retrieves all messages from the Reddit inbox of the authenticated user. It returns a list of dictionaries, where each dictionary represents a message and contains the following keys: id, subject, body, sender, time, and replies. The replies key corresponds to a list of replies to the message, where each reply is represented as a dictionary with the keys id, body, sender, and time.
# send_message(username, subject, body): This function sends a message to a specified Reddit user. The parameters are:
# username: The username of the recipient.
# subject: The subject of the message.
# body: The body of the message. Note that the username is currently hardcoded to ‘NadeemGorsi’ to avoid sending test messages to real users.
# reply_to_message_by_id(message_id, body): This function sends a reply to a specific message in the Reddit inbox of the authenticated user. The parameters are:
# message_id: The ID of the message to reply to.
# body: The body of the reply.

# create_thread(): This function creates a new thread using the OpenAI API and returns the ID of the created thread. No parameters are needed for this function.
# add_message(message, threadId): This function adds a new message to a specific thread. The parameters are:
# message: The content of the message to be added.
# threadId: The ID of the thread where the message will be added. The function sets the role of the message to “user”.
# get_thread_messages(threadId): This function retrieves all messages from a specific thread. The parameter is:
# threadId: The ID of the thread from which to retrieve the messages. The function prints the ID, thread ID, and content of each message, and returns the list of messages.

# create_tables(): Initializes the SQLite database and creates the necessary tables. The tables include posts, messages, and reddit_auth.
# insert_post(post): Inserts a new post into the posts table. The post parameter is a dictionary with keys corresponding to the fields in the posts table.
# get_posts(admin=None): Retrieves posts from the posts table. If an admin username is provided, it retrieves only the posts associated with that admin. If no admin is provided, it retrieves all posts.
# insert_message(post_id, message, message_id, source): Inserts a new message into the messages table. The parameters are the ID of the associated post, the message text, the message ID, and the source of the message.
# update_openai_thread_id(post_id, openai_thread_id): Updates the OpenAI thread ID of a specific post in the posts table. The parameters are the post ID and the new OpenAI thread ID.
# update_reddit_message_id(post_id, reddit_message_id): Updates the Reddit message ID of a specific post in the posts table. The parameters are the post ID and the new Reddit message ID.
# check_message_status(post_id): Checks the message status of a specific post in the posts table. The parameter is the post ID.
# update_message_status(post_id, status): Updates the message status of a specific post in the posts table. The parameters are the post ID and the new status.
# mark_message_replied(message_id): Marks a specific message as replied in the messages table. The parameter is the message ID.
# insert_reddit_auth(admin_username, refresh_token): Inserts or updates the Reddit authentication details of a specific admin in the reddit_auth table. The parameters are the admin username and the refresh token.
# get_reddit_auth(admin_username): Retrieves the Reddit refresh token of a specific admin from the reddit_auth table. The parameter is the admin username.



# posts table:
# id: TEXT, PRIMARY KEY. A unique identifier for each post.
# title: TEXT. The title of the post.
# text: TEXT. The text content of the post.
# html: TEXT. The HTML content of the post.
# author: TEXT. The author of the post.
# subreddit: TEXT. The subreddit where the post was made.
# post_url: TEXT. The URL of the post.
# admin: TEXT. The admin who is handling the post.
# openai_thread_id: TEXT. The ID of the OpenAI thread associated with the post.
# reddit_message_id: TEXT. The ID of the Reddit message associated with the post.
# message_status: TEXT. The status of the message. It can be ‘waiting_for_assistant’ or ‘waiting_for_user’.
# messages table:
# id: INTEGER, PRIMARY KEY, AUTOINCREMENT. A unique identifier for each message.
# post_id: TEXT. The ID of the post associated with the message.
# message: TEXT. The text content of the message.
# message_id: TEXT, UNIQUE. A unique identifier for each message.
# source: TEXT. The source of the message, either ‘openai’ or ‘reddit’.
# timestamp: DATETIME, DEFAULT CURRENT_TIMESTAMP. The timestamp when the message was created.
# replied: INTEGER, DEFAULT 0. A flag indicating whether the message has been replied to.
