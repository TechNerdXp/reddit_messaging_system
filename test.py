import praw
from pprint import pprint

def reddit_posts(subreddit_name, limit=10):
    reddit = praw.Reddit(
        client_id='ziA4CfKVB5fwlDv83r05JA',
        client_secret='qiznFKcderMXwmhVuzPbgExbnFc4bQ',
        user_agent='web:com.technerdxp.redditfilter:v1.0 (by /u/technerdxp)'
    )

    subreddit = reddit.subreddit(subreddit_name)
    top_posts = subreddit.hot(limit=limit)

    for post in top_posts:
        pprint(f'@{post.author.name}')
        pprint(vars(post))


if __name__ == '__main__':
    reddit_posts('Python', limit=1)  # Example usage
    
