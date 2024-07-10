import os 
from dotenv import load_dotenv
from openai import OpenAI
from batch_config import OUTPUT

FILE = "?"


def main():
    load_dotenv()
    client = OpenAI(
        organization=os.getenv("OPENAI_PROJECT"),
        project=os.getenv("OPENAI_PROJECT"),
        api_key=os.getenv("OPENAI_API_KEY"),
    )

    content = client.files.content(FILE)

    with open(OUTPUT, "wb", encoding="utf-8") as _file:
        _file.write(content)


if __name__ == "__main__":
    main()
