import sys
import time
from dotenv import load_dotenv
from utils.cost import estimate_costs, get_costs_gpt4o, get_n_tokens
from utils.utils import ask_permission
from utils.ai import query_gpt, get_prompt


INPUT = "output/1717274042.txt"
OUTPUT = f"output/{int(time.time())}_ai.txt"
AI_MODEL = "gpt-4o"


PROMPT = """This text was transcribed by OCR. Your job is to fix obvious transcription errors, such as problems with word separation, punctuation, encoding. Output only the corrected text. Only correct issues which would be generated by a bad transcription. Don't correct stylistic choices, local accents or the logical flow of sentences. Answer in Markdown.

###

Text: 

{snippet}

###

Answer:
"""


def ai_cleanup(text: str) -> str:
    load_dotenv()

    prompt = get_prompt(PROMPT, text)
    model = AI_MODEL

    n_tokens = get_n_tokens(model, prompt)
    estimate_costs(model, n_tokens)

    if not ask_permission():
        sys.exit(0)

    try:
        response = query_gpt(model, prompt)
    except Exception as e:
        print(e)
        return e.__repr__()

    get_costs_gpt4o(response)

    return response.choices[0].message.content  # type: ignore


def main():
    with open(INPUT, "r", encoding="utf-8") as _input:
        text = _input.read()

    result = ai_cleanup(text)

    with open(OUTPUT, "w", encoding="utf-8") as _output:
        _output.write(result)
        print("Antiquarian: cleanup complete. Output written to", OUTPUT)


if __name__ == "__main__":
    main()
