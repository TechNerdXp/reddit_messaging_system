# if need ot make author field unique.
import sqlite3

def update_table():
    conn = sqlite3.connect('db/reddit_messaging_sys.db')
    c = conn.cursor()

    # Create new table with UNIQUE constraint
    c.execute('''
        CREATE TABLE IF NOT EXISTS new_posts
        (id INTEGER PRIMARY KEY AUTOINCREMENT,
        post_id TEXT UNIQUE,
        title TEXT,
        text TEXT,
        html TEXT,
        author TEXT Unique,
        subreddit TEXT,
        post_url TEXT,
        admin TEXT,
        openai_thread_id TEXT,
        reddit_message_id TEXT,
        created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
        updated_at DATETIME DEFAULT CURRENT_TIMESTAMP,
        message_status TEXT DEFAULT 'thread_not_started')
    ''')

    # Copy distinct records from old table to new table
    c.execute('''
        INSERT INTO new_posts(post_id, title, text, html, author, subreddit, post_url, admin, openai_thread_id, reddit_message_id, created_at, updated_at, message_status)
        SELECT post_id, title, text, html, author, subreddit, post_url, admin, openai_thread_id, reddit_message_id, created_at, updated_at, message_status
        FROM (
            SELECT *, ROW_NUMBER() OVER (PARTITION BY author ORDER BY id) AS rn
            FROM posts
        )
        WHERE rn = 1
    ''')

    # Drop old table
    c.execute('DROP TABLE posts')

    # Rename new table to old table
    c.execute('ALTER TABLE new_posts RENAME TO posts')

    conn.commit()
    conn.close()
