import praw

def reddit_posts(subreddit_name, limit=10, postType='top'):
    reddit = praw.Reddit(
        client_id='ziA4CfKVB5fwlDv83r05JA',
        client_secret='qiznFKcderMXwmhVuzPbgExbnFc4bQ',
        user_agent='web:com.technerdxp.redditfilter:v1.0 (by /u/technerdxp)'
    )

    subreddit = reddit.subreddit(subreddit_name)
    if postType == 'hot':
        posts = subreddit.hot(limit=limit)
    elif postType == 'new':
        posts = subreddit.new(limit=limit)
    elif postType == 'controversial':
        posts = subreddit.controversial(limit=limit)
    elif postType == 'rising':
        posts = subreddit.rising(limit=limit)
    else:
        posts = subreddit.top(limit=limit)
        
    posts_data = []
    for post in posts:
        posts_data.append({'id':post.id, 'title': post.title, 'text': post.selftext, 'html': post.selftext_html, 'author': f'@{post.author.name}', 'subreddit': post.subreddit.display_name, 'post_url': post.url})
    return posts_data
