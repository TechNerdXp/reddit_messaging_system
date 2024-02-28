from fuzzywuzzy import fuzz
from project_logger import logger

def filter_posts(posts, keywords, exactMatch, fuzz_ratio=80):
    if keywords == []:
        return posts
    
    filtered_posts = []
    for post in posts:
        for keyword in keywords:
            if exactMatch:
                if keyword.lower() in post['title'].lower() or keyword.lower() in post['text'].lower():
                    filtered_posts.append(post)
                    break
            else:
                if max(fuzz.partial_ratio(keyword.lower(), word.lower()) for word in post['title'].split() + post['text'].split()) >= fuzz_ratio:
                    filtered_posts.append(post)
                    break
    return filtered_posts
