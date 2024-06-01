from openai import OpenAI


# @retry(tries=10, delay=1, backoff=2)
def query_gpt(model: str, prompt: str):
    client = OpenAI()

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
