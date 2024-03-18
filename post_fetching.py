import time
from project_logger import logger
from reddit import reddit_posts, create_reddit_instance, is_authenticated
from project_db import insert_post, insert_user, get_admins_and_subreddits




def fetch_posts():
    admin_subreddits = get_admins_and_subreddits()
    for row in admin_subreddits:
        admin = row['username']
        if not is_authenticated(admin)['success']:
            print(f'{admin} is not authenticated. Pls authenticate using UI')
            logger.error(f'{admin} is not authenticated. Pls authenticate using UI')
            continue

        reddit = create_reddit_instance(admin)
        
        subreddits = [subreddit.strip() for subreddit in row['subreddits'].split(',')]
        keywords = [keyword.strip() for keyword in row['keywords'].split(',')]
        for subreddit in subreddits:
            print(f'<<<<<< Fetching posts from r/{subreddit} for u/{admin} >>>>>>')
            posts = reddit_posts(admin, subreddit, keywords, reddit)
            for post in posts:
                insert_post(post)
                insert_user(post['author'])    
                           
        
if __name__ == '__main__':
    while True:
        try:
            fetch_posts()
        except Exception as e:
            print(str(e))
            logger.error(str(e))
        time.sleep(300)
