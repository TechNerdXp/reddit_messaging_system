import sqlite3
import os

if not os.path.exists('logs'):
    os.makedirs('logs')
    
def create_tables():
    conn = sqlite3.connect('db/reddit_messaging_sys.db')
    c = conn.cursor()

    c.execute('''
        CREATE TABLE IF NOT EXISTS posts
        (id TEXT PRIMARY KEY,
        title TEXT,
        text TEXT,
        html TEXT,
        author TEXT,
        subreddit TEXT,
        post_url TEXT,
        admin TEXT,
        openai_thread_id TEXT,
        reddit_message_id TEXT)
    ''')

    # c.execute('''
    #     CREATE TABLE IF NOT EXISTS users
    #     (username TEXT PRIMARY KEY)
    # ''')

    
    c.execute('''
        CREATE TABLE IF NOT EXISTS reddit_auth
        (admin_username TEXT PRIMARY KEY,
        refresh_token TEXT)
    ''')
    
    c.execute('''
        CREATE TABLE IF NOT EXISTS openai_messages
        (id INTEGER PRIMARY KEY AUTOINCREMENT,
        post_id TEXT,
        message TEXT,
        message_id TEXT UNIQUE,
        timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
        replied INTEGER DEFAULT 0,
        FOREIGN KEY(post_id) REFERENCES posts(id))
    ''')

    c.execute('''
        CREATE TABLE IF NOT EXISTS reddit_messages
        (id INTEGER PRIMARY KEY AUTOINCREMENT,
        post_id TEXT,
        message TEXT,
        message_id TEXT UNIQUE,
        timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
        replied INTEGER DEFAULT 0,
        FOREIGN KEY(post_id) REFERENCES posts(id))
    ''')


    conn.commit()
    conn.close()


def insert_post(post):
    conn = sqlite3.connect('db/reddit_messaging_sys.db')
    c = conn.cursor()

    c.execute('''
        INSERT OR IGNORE INTO posts VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    ''', (post['id'], post['title'], post['text'], post['html'], post['author'], post['subreddit'], post['post_url'], post['admin']))

    conn.commit()
    conn.close()

def get_posts():
    conn = sqlite3.connect('db/reddit_messaging_sys.db')
    conn.row_factory = sqlite3.Row

    c = conn.cursor()

    c.execute('SELECT * FROM posts')
    posts = c.fetchall()

    conn.close()

    posts = [dict(row) for row in posts]

    return posts


def insert_reddit_auth(admin_username, refresh_token):
    conn = sqlite3.connect('db/reddit_messaging_sys.db')
    c = conn.cursor()

    c.execute('''
        INSERT OR REPLACE INTO reddit_auth VALUES (?, ?)
    ''', (admin_username, refresh_token))

    conn.commit()
    conn.close()

def get_reddit_auth(admin_username):
    conn = sqlite3.connect('db/reddit_messaging_sys.db')
    c = conn.cursor()

    c.execute('SELECT refresh_token FROM reddit_auth WHERE admin_username = ?', (admin_username,))
    result = c.fetchone()

    conn.close()

    return result[0] if result else None

def update_openai_thread_id(post_id, openai_thread_id):
    conn = sqlite3.connect('db/reddit_messaging_sys.db')
    c = conn.cursor()

    c.execute('''
        UPDATE posts SET openai_thread_id = ? WHERE id = ?
    ''', (openai_thread_id, post_id))

    conn.commit()
    conn.close()

def update_reddit_message_id(post_id, reddit_message_id):
    conn = sqlite3.connect('db/reddit_messaging_sys.db')
    c = conn.cursor()

    c.execute('''
        UPDATE posts SET reddit_message_id = ? WHERE id = ?
    ''', (reddit_message_id, post_id))

    conn.commit()
    conn.close()

def insert_openai_message(post_id, message, message_id):
    conn = sqlite3.connect('db/reddit_messaging_sys.db')
    c = conn.cursor()

    # Insert a message into openai_messages and ignore if the message_id already exists
    c.execute('''
        INSERT OR IGNORE INTO openai_messages
        (post_id, message, message_id)
        VALUES (?, ?, ?)
    ''', (post_id, message, message_id))

    conn.commit()
    conn.close()

def insert_reddit_message(post_id, message, message_id):
    conn = sqlite3.connect('db/reddit_messaging_sys.db')
    c = conn.cursor()

    # Insert a message into reddit_messages and ignore if the message_id already exists
    c.execute('''
        INSERT OR IGNORE INTO reddit_messages
        (post_id, message, message_id)
        VALUES (?, ?, ?)
    ''', (post_id, message, message_id))

    conn.commit()
    conn.close()

def mark_openai_message_replied(message_id):
    conn = sqlite3.connect('db/reddit_messaging_sys.db')
    c = conn.cursor()

    # Mark a message as replied in openai_messages
    c.execute('''
        UPDATE openai_messages
        SET replied = 1
        WHERE message_id = ?
    ''', (message_id,))

    conn.commit()
    conn.close()

def mark_reddit_message_replied(message_id):
    conn = sqlite3.connect('db/reddit_messaging_sys.db')
    c = conn.cursor()

    # Mark a message as replied in reddit_messages
    c.execute('''
        UPDATE reddit_messages
        SET replied = 1
        WHERE message_id = ?
    ''', (message_id,))

    conn.commit()
    conn.close()











def insert_user(username):
    conn = sqlite3.connect('db/reddit_messaging_sys.db')
    c = conn.cursor()

    c.execute('''
        INSERT OR IGNORE INTO users VALUES (?)
    ''', (username,))

    conn.commit()
    conn.close()

def get_users():
    conn = sqlite3.connect('db/reddit_messaging_sys.db')
    c = conn.cursor()

    c.execute('SELECT * FROM users')
    users = c.fetchall()

    conn.close()

    return users

def insert_message(message):
    conn = sqlite3.connect('db/reddit_messaging_sys.db')
    c = conn.cursor()

    c.execute('''
        INSERT INTO messages VALUES (?, ?, ?, ?, ?)
    ''', (message['id'], message['post_id'], message['username'], message['sender'], message['content']))

    conn.commit()
    conn.close()

def get_messages_for_post(post_id):
    conn = sqlite3.connect('db/reddit_messaging_sys.db')
    c = conn.cursor()

    c.execute('SELECT * FROM messages WHERE post_id = ?', (post_id,))
    messages = c.fetchall()

    conn.close()

    return messages

def get_messages_for_user(username):
    conn = sqlite3.connect('db/reddit_messaging_sys.db')
    c = conn.cursor()

    c.execute('SELECT * FROM messages WHERE username = ?', (username,))
    messages = c.fetchall()

    conn.close()

    return messages

create_tables()