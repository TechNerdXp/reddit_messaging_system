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
    
def get_reddit_reply_id(post_id):
    conn = sqlite3.connect('db/reddit_messaging_sys.db')
    c = conn.cursor()

    c.execute('SELECT reddit_reply_id FROM posts WHERE id = ?', (post_id,))
    result = c.fetchone()
    conn.close()
    return result[0] if result else None
    
def check_message_status(post_id):
    conn = sqlite3.connect('db/reddit_messaging_sys.db')
    c = conn.cursor()

    # Check the message_status of a post
    c.execute('''
        SELECT message_status
        FROM posts
        WHERE id = ?
    ''', (post_id,))

    status = c.fetchone()[0]

    conn.close()

    return status

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
    
def insert_message(post_id, message, message_id, source):
    conn = sqlite3.connect('db/reddit_messaging_sys.db')
    c = conn.cursor()

    # Insert a message and ignore if the message_id already exists
    c.execute('''
        INSERT OR IGNORE INTO messages
        (post_id, message, message_id, source)
        VALUES (?, ?, ?, ?)
    ''', (post_id, message, message_id, source))

    conn.commit()
    conn.close()
    
def message_exists(message_id):
    conn = sqlite3.connect('db/reddit_messaging_sys.db')
    c = conn.cursor()

    c.execute('SELECT id FROM messages WHERE message_id = ?', (message_id,))
    result = c.fetchone()

    conn.close()

    return result is not None
    
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

    c.execute("INSERT OR IGNORE INTO configs (key, value) VALUES (?, ?)", (key, value))
    c.execute("UPDATE configs SET value=? WHERE key=?", (value, key))

    conn.commit()
    conn.close()

def insert_initial_configs():
    configs = [
        ('REDDIT_RATE_LIMIT', '30'),
        ('DELAY_BETWEEN_MESSAGES', '200'),
        ('REDDIT_ADMINS', 'Heydrianpay,Partsnetwork878,hghgj67,TechNerdXp,NadeemGorsi'),
    ]
    for key, value in configs:
        update_config(key, value)

create_tables()




# def get_users():
#     conn = sqlite3.connect('db/reddit_messaging_sys.db')
#     c = conn.cursor()

#     c.execute('SELECT * FROM users')
#     users = c.fetchall()

#     conn.close()

#     return users

# def insert_message(message):
#     conn = sqlite3.connect('db/reddit_messaging_sys.db')
#     c = conn.cursor()

#     c.execute('''
#         INSERT INTO messages VALUES (?, ?, ?, ?, ?)
#     ''', (message['id'], message['post_id'], message['username'], message['sender'], message['content']))

#     conn.commit()
#     conn.close()

# def get_messages_for_post(post_id):
#     conn = sqlite3.connect('db/reddit_messaging_sys.db')
#     c = conn.cursor()

#     c.execute('SELECT * FROM messages WHERE post_id = ?', (post_id,))
#     messages = c.fetchall()

#     conn.close()

#     return messages

# def get_messages_for_user(username):
#     conn = sqlite3.connect('db/reddit_messaging_sys.db')
#     c = conn.cursor()

#     c.execute('SELECT * FROM messages WHERE username = ?', (username,))
#     messages = c.fetchall()

#     conn.close()

#     return messages