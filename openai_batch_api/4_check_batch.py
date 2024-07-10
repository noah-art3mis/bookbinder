import os
from dotenv import load_dotenv
from openai import OpenAI
from batch_config import BATCH_ID
from pprint import pprint


def main():
    load_dotenv()
    client = OpenAI(
        organization=os.getenv("OPENAI_PROJECT"),
        project=os.getenv("OPENAI_PROJECT"),
        api_key=os.getenv("OPENAI_API_KEY"),
    )
    # list = client.batches.list()
    # pprint(vars(list))
    # print()
    res = client.batches.retrieve(BATCH_ID)
    pprint(vars(res))


if __name__ == "__main__":
    main()
