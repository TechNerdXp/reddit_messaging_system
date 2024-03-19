from datetime import datetime
import sqlite3
import os

if not os.path.exists('db'):
    os.makedirs('db')
    
def create_tables():
    conn = sqlite3.connect('db/reddit_messaging_sys.db')
    c = conn.cursor()

    c.execute('''
        CREATE TABLE IF NOT EXISTS posts
        (id INTEGER PRIMARY KEY AUTOINCREMENT,
        post_id TEXT UNIQUE,
        title TEXT,
        text TEXT,
        html TEXT,
        author TEXT,
        subreddit TEXT,
        post_url TEXT,
        admin TEXT,
        openai_thread_id TEXT,
        reddit_message_id TEXT,
        created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
        updated_at DATETIME DEFAULT CURRENT_TIMESTAMP,
        message_status TEXT DEFAULT 'thread_not_started')
    ''')

    c.execute('''
        CREATE TABLE IF NOT EXISTS users
        (username TEXT PRIMARY KEY)
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
        INSERT OR IGNORE INTO posts (post_id, title, text, html, author, subreddit, post_url, admin) VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    ''', (post['id'], post['title'], post['text'], post['html'], post['author'], post['subreddit'], post['post_url'], post['admin']))

    conn.commit()
    conn.close()

def get_posts(admin=None, limit=None):
    conn = sqlite3.connect('db/reddit_messaging_sys.db')
    conn.row_factory = sqlite3.Row

    c = conn.cursor()

    if admin is None:
        query = 'SELECT * FROM posts ORDER BY updated_at DESC'
    else:
        query = 'SELECT * FROM posts WHERE admin = ? ORDER BY updated_at DESC'

    if limit is not None:
        query += ' LIMIT ?'
        c.execute(query, (admin, limit) if admin else (limit,))
    else:
        c.execute(query, (admin,) if admin else ())

    posts = c.fetchall()

    conn.close()

    posts = [dict(row) for row in posts]

    return posts

def update_openai_thread_id(post_id, openai_thread_id):
    conn = sqlite3.connect('db/reddit_messaging_sys.db')
    c = conn.cursor()

    c.execute('''
        UPDATE posts SET openai_thread_id = ?, updated_at = ? WHERE post_id = ?
    ''', (openai_thread_id, datetime.now(), post_id))

    conn.commit()
    conn.close()

def update_reddit_message_id(post_id, reddit_message_id):
    conn = sqlite3.connect('db/reddit_messaging_sys.db')
    c = conn.cursor()

    c.execute('''
        UPDATE posts SET reddit_message_id = ?, updated_at = ? WHERE post_id = ?
    ''', (reddit_message_id, datetime.now(), post_id))

    conn.commit()
    conn.close()

def update_message_status(post_id, status):
    conn = sqlite3.connect('db/reddit_messaging_sys.db')
    c = conn.cursor()

    c.execute('''
        UPDATE posts
        SET message_status = ?, updated_at = ?
        WHERE post_id = ?
    ''', (status, datetime.now(), post_id))

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

    configs = {row['key']: row['value'] for row in rows}

    conn.close()

    return configs
    
def get_config(key):
    conn = sqlite3.connect('db/reddit_messaging_sys.db')
    c = conn.cursor()

    c.execute('SELECT value FROM configs WHERE key=?', (key,))
    result = c.fetchone()

    conn.close()

    if result is None:
        return None
    else:
        return result[0]

def update_config(key, value):
    conn = sqlite3.connect('db/reddit_messaging_sys.db')
    c = conn.cursor()
    c.execute('UPDATE configs SET value=? WHERE key=?', (value, key))

    conn.commit()
    conn.close()

def insert_initial_configs(configs):
    conn = sqlite3.connect('db/reddit_messaging_sys.db')
    c = conn.cursor()
    for key, value in configs:
        c.execute('INSERT OR IGNORE INTO configs (key, value) VALUES (?, ?)', (key, value))
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
    
def insert_default_admin():
    insert_admin_and_subreddit('TechNerdXp', 'Test, Best', 'Hello, Hi, Test, Good Morning')
