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
        post_url TEXT),
        admin TEXT)
    ''')

    c.execute('''
        CREATE TABLE IF NOT EXISTS users
        (username TEXT PRIMARY KEY)
    ''')

    c.execute('''
        CREATE TABLE IF NOT EXISTS messages
        (id TEXT PRIMARY KEY,
        post_id TEXT REFERENCES posts(id),
        username TEXT REFERENCES users(username),
        sender TEXT,
        content TEXT)
    ''')
    
    c.execute('''
        CREATE TABLE IF NOT EXISTS reddit_auth
        (username TEXT PRIMARY KEY,
        refresh_token TEXT)
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

def insert_reddit_auth(username, refresh_token):
    conn = sqlite3.connect('db/reddit_messaging_sys.db')
    c = conn.cursor()

    c.execute('''
        INSERT OR REPLACE INTO reddit_auth VALUES (?, ?)
    ''', (username, refresh_token))

    conn.commit()
    conn.close()

def get_reddit_auth(username):
    conn = sqlite3.connect('db/reddit_messaging_sys.db')
    c = conn.cursor()

    c.execute('SELECT refresh_token FROM reddit_auth WHERE username = ?', (username,))
    result = c.fetchone()

    conn.close()

    return result[0] if result else None


create_tables()