import os
from dotenv import load_dotenv
from openai import OpenAI
from batch_config import FILE_ID
from pprint import pprint


def main():
    load_dotenv()
    client = OpenAI(
        organization=os.getenv("OPENAI_PROJECT"),
        project=os.getenv("OPENAI_PROJECT"),
        api_key=os.getenv("OPENAI_API_KEY"),
    )

    res = client.batches.create(
        input_file_id=FILE_ID,
        endpoint="/v1/chat/completions",
        completion_window="24h",
        metadata={"description": "STJ_3911"},
    )
    pprint(vars(res))


if __name__ == "__main__":
    main()
