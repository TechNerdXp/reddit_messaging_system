from project_db import get_admins_and_subreddits, get_admins_list

admin_subreddits = get_admins_and_subreddits()
    
for row in admin_subreddits:
    admin = row['username']
    subreddits = row['subreddits'].split()
    keywords = row['keywords'].split()
    for subreddit in subreddits:
        print(admin)
        print(subreddit)
        print(keywords)
        print('___________________________')