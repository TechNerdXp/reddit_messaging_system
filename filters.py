from fuzzywuzzy import fuzz

def filter_posts(posts, keywords, exactMatch, fuzz_ratio=80):
    keywords = keywords.split()
    filtered_posts = []
    for post in posts:
        for keyword in keywords:
            if exactMatch:
                if keyword in post['title'].split() or keyword in post['text'].split():
                    filtered_posts.append(post)
                    break
            else:
                if max(fuzz.partial_ratio(keyword, word) for word in post['title'].split() + post['text'].split()) >= fuzz_ratio:
                    filtered_posts.append(post)
                    break
    return filtered_posts
