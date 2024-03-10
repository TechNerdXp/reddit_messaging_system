from ai import get_thread_messages

messages = get_thread_messages('thread_hXiw2wGK2126ZGNx06ng2FCT')

# for message in messages.data:
#         print(message.role)
#         print(message.content[0].text.value)

import json

admin_subreddits = {
    'TechNerdXp': {
        'Java': ['ai', 'machine learning'],
        'Python': ['ai', 'machine learning']
    },
    'Heydrianpay': {
        'AskMechanics': ['My car won\'t start', 'an issue with my car', 'my car is making a noise', 'transmission issue', 'knocking sound', 'crank no start'],
    },
}

# Save to JSON file
with open('admin_subreddits.json', 'w') as f:
    json.dump(admin_subreddits, f)

# Load from JSON file
with open('admin_subreddits.json', 'r') as f:
    loaded_admin_subreddits = json.load(f)

print(loaded_admin_subreddits)
