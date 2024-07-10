import os 
from dotenv import load_dotenv
from openai import OpenAI
from batch_config import BATCH_FILE
from pprint import pprint

def main():
    load_dotenv()
    client = OpenAI(
        organization=os.getenv("OPENAI_PROJECT"),
        project=os.getenv("OPENAI_PROJECT"),
        api_key=os.getenv("OPENAI_API_KEY"),
    )

    batch_input_file = client.files.create(
        file=open(BATCH_FILE, "rb"),
        purpose="batch",
    )
    pprint(vars(batch_input_file))


if __name__ == "__main__":
    main()
