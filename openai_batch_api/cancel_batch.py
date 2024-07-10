from openai import OpenAI
import os 
from dotenv import load_dotenv


def main():
    load_dotenv()
    client = OpenAI(
        organization=os.getenv("OPENAI_PROJECT"),
        project=os.getenv("OPENAI_PROJECT"),
        api_key=os.getenv("OPENAI_API_KEY"),
    )
    
    res = client.batches.cancel(BATCH)


if __name__ == "__main__":
    main()
