import pandas as pd
import numpy as np
import json
import tiktoken
from batch_config import INPUT, OUTPUT, PROMPT, AI_MODEL


def generate_batch_item(model: str, prompt: str, variable: str, id: str) -> object:

    message = prompt.replace("{variable}", variable)
    messages = [{"role": "user", "content": message}]

    return {
        "custom_id": id,
        "method": "POST",
        "url": "/v1/chat/completions",
        "body": {
            "model": model,
            "messages": messages,
            "max_tokens": 4000,
        },
    }


def generate_batch(df: pd.DataFrame, output: str, model: str, prompt: str) -> None:
    with open(output, "w", encoding="utf-8") as outfile:
        for i, v in enumerate(df["decisao"]):
            _id = str(f"{i:04}")

            item = generate_batch_item(
                model=model,
                prompt=prompt,
                variable=v,
                id=_id,
            )
            outfile.write(json.dumps(item) + "\n")


def check_batch_cost(model: str, output: str) -> None:
    with open(output, "r", encoding="utf-8") as _file:
        batched = _file.readlines()

        costs = 0
        for item in batched:
            js = json.loads(item.strip())
            content = str(js["body"]["messages"])
            costs += estimate_batch_costs(model, content)
        print(f"Cost Estimation: just the input will cost {costs:.2f}")


def estimate_batch_costs(model: str, content: str) -> float:
    OMNI_INPUT = 5 / 1_000_000
    OMNI_OUTPUT = 15 / 1_000_000

    if model == "gpt-4o":
        MODEL_INPUT = OMNI_INPUT
    else:
        raise ValueError("Model not supported.")

    n_tokens = get_n_tokens(model, content)
    input_cost = n_tokens * MODEL_INPUT

    # batch discount
    input_cost = input_cost / 2
    return input_cost


def get_n_tokens(model: str, text: str) -> int:
    encoding = tiktoken.encoding_for_model(model)
    tokenized = encoding.encode(text)
    n_tokens = len(tokenized)
    return n_tokens


def main():
    df = pd.read_csv(INPUT)
    generate_batch(df, OUTPUT, AI_MODEL, PROMPT)
    check_batch_cost(AI_MODEL, OUTPUT)


if __name__ == "__main__":
    main()
