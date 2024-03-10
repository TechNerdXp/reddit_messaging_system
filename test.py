# from ai import get_thread_messages
# messages = get_thread_messages('thread_hXiw2wGK2126ZGNx06ng2FCT')

# for message in messages.data:
#         print(message.role)
#         print(message.content[0].text.value)

from project_db import insert_initial_configs
insert_initial_configs()
