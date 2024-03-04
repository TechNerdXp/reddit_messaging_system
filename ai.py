import os
from dotenv import load_dotenv
from openai import OpenAI
load_dotenv()

assistant_id = os.getenv("OPENAI_ASSISTENT_ID")
client = OpenAI(
  api_key=os.getenv("OPENAI_API_KEY"),
)

def create_thread():
    thread = client.beta.threads.create()
    return thread.id

def add_message(message, threadId):
    message = client.beta.threads.messages.create(
        thread_id=threadId,
        role="user",
        content= message
    )
    return message.id
    
def run_assistant(threadId):
    run = client.beta.threads.runs.create(
        thread_id=threadId,
        assistant_id=assistant_id,
        instructions=""
    )
    return run.id

def check_run_status(threadId, runId):
    run = client.beta.threads.runs.retrieve(
        thread_id=threadId,
        run_id=runId
    )
    return run.status
    
def get_thread_messages(threadId):
    messages = client.beta.threads.messages.list(
        thread_id=threadId
    )
    for message in messages.data:
        print("Message ID:", message.id)
        print("Thread ID:", message.thread_id)
        print("Message Content:", message.content[0].text.value)
        print('.................................................')
        # print(messages)
    return messages


# print(create_thread())
add_message('test message', 'thread_j4b3JCffZYbuFt3vb1Zj0RAT')
# print(run_assistant('thread_j4b3JCffZYbuFt3vb1Zj0RAT'))
# check_run_status('thread_j4b3JCffZYbuFt3vb1Zj0RAT', 'run_pA03itrIt6aIo9gQCkTlpkJK')
# get_thread_messages('thread_j4b3JCffZYbuFt3vb1Zj0RAT')