from openai import OpenAI
import os
from dotenv import load_dotenv


# @retry(tries=10, delay=1, backoff=2)
def query_gpt(model: str, prompt: str):
    load_dotenv()
    client = OpenAI(
        organization=os.getenv("OPENAI_PROJECT"),
        project=os.getenv("OPENAI_PROJECT"),
        api_key=os.getenv("OPENAI_API_KEY"),
    )

    message = client.chat.completions.create(
        model=model,
        temperature=0,
        messages=get_messages(prompt),  # type: ignore
    )
    return message


def get_prompt(prompt, snippet: str) -> str:
    return prompt.replace("{snippet}", snippet)


def get_messages(prompt: str):
    messages = []
    message = {"role": "user", "content": prompt}
    messages.append(message)
    return messages
