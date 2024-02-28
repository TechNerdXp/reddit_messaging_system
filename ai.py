import os
from dotenv import load_dotenv
import openai
load_dotenv()

def call_assistant(message):
    openai.api_key = os.getenv("OPENAI_API_KEY")
    assistant_id = os.getenv("OPENAI_ASSISTENT_ID")

    response = openai.Assistant.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": message},
        ],
        assistant_id=assistant_id,
    )

    return response['choices'][0]['message']['content']

# Example usage:
response = call_assistant("Hello, assistant!")
print(response)
