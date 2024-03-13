import sqlite3
import os

if not os.path.exists('db'):
    os.makedirs('db')
    
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
        reddit_message_id TEXT,
        reddit_reply_id TEXT,
        message_status TEXT DEFAULT 'thread_not_started')
    ''')

    c.execute('''
        CREATE TABLE IF NOT EXISTS users
        (username TEXT PRIMARY KEY)
    ''')

    # Create table for messages
    c.execute('''
        CREATE TABLE IF NOT EXISTS messages
        (id INTEGER PRIMARY KEY AUTOINCREMENT,
        post_id TEXT,
        message TEXT,
        message_id TEXT,
        source TEXT,
        timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY(post_id) REFERENCES posts(id))
    ''')
    
    c.execute('''
        CREATE TABLE IF NOT EXISTS reddit_auth
        (admin_username TEXT PRIMARY KEY,
        refresh_token TEXT)
    ''')
    
    c.execute('''
        CREATE TABLE IF NOT EXISTS configs
        (key TEXT PRIMARY KEY,
        value TEXT)
    ''')
    
    c.execute('''
        CREATE TABLE IF NOT EXISTS admins_and_subreddits
        (id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT UNIQUE,
        subreddits TEXT,
        keywords TEXT)
    ''')
    
    # ids of messages from the assistant
    c.execute('''
        CREATE TABLE IF NOT EXISTS assistant_messages
        (id INTEGER PRIMARY KEY AUTOINCREMENT,
        assistant_message_id TEXT UNIQUE)
    ''')
    
    # ids of messages from reddit
    c.execute('''
        CREATE TABLE IF NOT EXISTS reddit_messages
        (id INTEGER PRIMARY KEY AUTOINCREMENT,
        reddit_message_id TEXT UNIQUE)
    ''')              
    


    conn.commit()
    conn.close()

def insert_post(post):
    conn = sqlite3.connect('db/reddit_messaging_sys.db')
    c = conn.cursor()

    c.execute('''
        INSERT OR IGNORE INTO posts (id, title, text, html, author, subreddit, post_url, admin) VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    ''', (post['id'], post['title'], post['text'], post['html'], post['author'], post['subreddit'], post['post_url'], post['admin']))

    conn.commit()
    conn.close()

def get_posts(admin=None):
    conn = sqlite3.connect('db/reddit_messaging_sys.db')
    conn.row_factory = sqlite3.Row

    c = conn.cursor()

    if admin is None:
        # Select all posts if no admin is specified
        c.execute('SELECT * FROM posts')
    else:
        # Select posts for a specific admin
        c.execute('SELECT * FROM posts WHERE admin = ?', (admin,))

    posts = c.fetchall()

    conn.close()

    posts = [dict(row) for row in posts]

    return posts
    
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

def update_reddit_reply_id(post_id, reddit_reply_id):
    conn = sqlite3.connect('db/reddit_messaging_sys.db')
    c = conn.cursor()

    c.execute('''
        UPDATE posts SET reddit_reply_id = ? WHERE id = ?
    ''', (reddit_reply_id, post_id))

    conn.commit()
    conn.close()

def update_message_status(post_id, status):
    conn = sqlite3.connect('db/reddit_messaging_sys.db')
    c = conn.cursor()

    # Update the message_status of a post
    c.execute('''
        UPDATE posts
        SET message_status = ?
        WHERE id = ?
    ''', (status, post_id))

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

def get_configs():
    conn = sqlite3.connect('db/reddit_messaging_sys.db')
    conn.row_factory = sqlite3.Row
    c = conn.cursor()

    c.execute('SELECT * FROM configs')
    rows = c.fetchall()

    # Convert rows to a dictionary
    configs = {row['key']: row['value'] for row in rows}

    conn.close()

    return configs
    
def get_config(key):
    conn = sqlite3.connect('db/reddit_messaging_sys.db')
    c = conn.cursor()

    c.execute("SELECT value FROM configs WHERE key=?", (key,))
    result = c.fetchone()

    conn.close()

    if result is None:
        return None
    else:
        return result[0]

def update_config(key, value):
    conn = sqlite3.connect('db/reddit_messaging_sys.db')
    c = conn.cursor()
    c.execute("UPDATE configs SET value=? WHERE key=?", (value, key))

    conn.commit()
    conn.close()

def insert_initial_configs():
    configs = [
        ('REDDIT_POST_TYPE', 'new'),
        ('REDDIT_MAX_PAGES_PER_SUBREDDIT', '2'),
        ('REDDIT_RATE_LIMIT', '30'),
        ('DELAY_BETWEEN_MESSAGES', '200'),
    ]
    conn = sqlite3.connect('db/reddit_messaging_sys.db')
    c = conn.cursor()
    for key, value in configs:
        c.execute("INSERT OR IGNORE INTO configs (key, value) VALUES (?, ?)", (key, value))
    conn.commit()
    conn.close()
    
def insert_assistant_message_id(assistant_message_id):
    conn = sqlite3.connect('db/reddit_messaging_sys.db')
    c = conn.cursor()

    c.execute('''
        INSERT OR IGNORE INTO assistant_messages (assistant_message_id) VALUES (?)
    ''', (assistant_message_id,))

    conn.commit()
    conn.close()

def insert_reddit_message_id(reddit_message_id):
    conn = sqlite3.connect('db/reddit_messaging_sys.db')
    c = conn.cursor()

    c.execute('''
        INSERT OR IGNORE INTO reddit_messages (reddit_message_id) VALUES (?)
    ''', (reddit_message_id,))

    conn.commit()
    conn.close()

def assistant_message_id_exists(assistant_message_id):
    conn = sqlite3.connect('db/reddit_messaging_sys.db')
    c = conn.cursor()

    c.execute('''
        SELECT 1 FROM assistant_messages WHERE assistant_message_id = ?
    ''', (assistant_message_id,))

    exists = c.fetchone() is not None

    conn.close()

    return exists

def reddit_message_id_exists(reddit_message_id):
    conn = sqlite3.connect('db/reddit_messaging_sys.db')
    c = conn.cursor()

    c.execute('''
        SELECT 1 FROM reddit_messages WHERE reddit_message_id = ?
    ''', (reddit_message_id,))

    exists = c.fetchone() is not None

    conn.close()

    return exists

def insert_admin_and_subreddit(username, subreddits, keywords):
    conn = sqlite3.connect('db/reddit_messaging_sys.db')
    c = conn.cursor()

    c.execute('''
        INSERT OR IGNORE INTO admins_and_subreddits (username, subreddits, keywords) VALUES (?, ?, ?)
    ''', (username, subreddits, keywords))

    conn.commit()
    conn.close()

def get_admins_and_subreddits():
    conn = sqlite3.connect('db/reddit_messaging_sys.db')
    conn.row_factory = sqlite3.Row

    c = conn.cursor()

    c.execute('SELECT * FROM admins_and_subreddits')

    admins_and_subreddits = c.fetchall()

    conn.close()

    admins_and_subreddits = [dict(row) for row in admins_and_subreddits]

    return admins_and_subreddits

def get_admins_list():
    conn = sqlite3.connect('db/reddit_messaging_sys.db')
    c = conn.cursor()

    c.execute('SELECT username FROM admins_and_subreddits')

    admins = c.fetchall()

    conn.close()

    # Extract usernames from the tuples and convert them into a list
    admins = [admin[0] for admin in admins]

    return admins

    

def update_admin_and_subreddit(id, username, subreddits, keywords):
    conn = sqlite3.connect('db/reddit_messaging_sys.db')
    c = conn.cursor()

    c.execute('''
        UPDATE admins_and_subreddits SET username = ?, subreddits = ?, keywords = ? WHERE id = ?
    ''', (username, subreddits, keywords, id))

    conn.commit()
    conn.close()

def delete_admin_and_subreddit(id):
    conn = sqlite3.connect('db/reddit_messaging_sys.db')
    c = conn.cursor()

    c.execute('''
        DELETE FROM admins_and_subreddits WHERE id = ?
    ''', (id,))

    conn.commit()
    conn.close()


create_tables()
insert_initial_configs()
