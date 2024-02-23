import sqlite3

def create_table():
    conn = sqlite3.connect('reddit_posts.db')
    c = conn.cursor()

    c.execute('''
        CREATE TABLE IF NOT EXISTS posts
        (id TEXT PRIMARY KEY,
        title TEXT,
        text TEXT,
        html TEXT,
        author TEXT,
        subreddit TEXT,
        post_url TEXT)
    ''')

    conn.commit()
    conn.close()

def insert_post(post):
    conn = sqlite3.connect('reddit_posts.db')
    c = conn.cursor()

    c.execute('''
        INSERT INTO posts VALUES (?, ?, ?, ?, ?, ?, ?)
    ''', (post['id'], post['title'], post['text'], post['html'], post['author'], post['subreddit'], post['post_url']))

    conn.commit()
    conn.close()

def get_posts():
    conn = sqlite3.connect('reddit_posts.db')
    c = conn.cursor()

    c.execute('SELECT * FROM posts')
    posts = c.fetchall()

    conn.close()

    return posts
# OK, pls here is a situation pls try to understand!
# I've planned to communicate with the author of the post and chatGPT about each post.
# I've planned a conversations table or maybe 2 which ever is best 

# flow will look like this post content along with a prompt is sent to GTP and GPT response is then sent to the USER, then user response is sent to GTP and then GET response is sent to USER  I'm not sure about creating one or two conversations tables also how ot build relations shipp with the posts table etc. 

# pls lets focus on the DB flow for now. thanks!