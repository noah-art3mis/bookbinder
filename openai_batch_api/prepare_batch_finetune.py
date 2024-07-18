import os
import json
import tiktoken
import pandas as pd
from batch_config import (
    AI_MODEL,
    INPUT,
    PROMPT,
    BATCH_FILE,
    BATCH_SIZE_LIMIT,
)


def generate_finetune_item(system: str, question: str, answer: str) -> object:

    return {
        "messages": [
            {"role": "system", "content": system},
            {"role": "user", "content": question},
            {"role": "assistant", "content": answer},
        ]
    }


def generate_batch(
    df: pd.DataFrame, output_file: str, model: str, prompt: str, max_tokens: int
) -> None:
    current_file_index = 0
    current_file_tokens = 0
    current_file_data = []

    def write_current_file():
        nonlocal current_file_index, current_file_tokens, current_file_data

        if current_file_data:

            output_file_root = os.path.splitext(output_file)[0]
            file_name = f"{output_file_root}_{current_file_index:04}.jsonl"
            with open(file_name, "w", encoding="utf-8") as outfile:
                for index, item in enumerate(current_file_data):
                    if index == len(current_file_data) - 1:  # last item
                        outfile.write(json.dumps(item))
                    else:
                        outfile.write(json.dumps(item) + "\n")

            current_file_index += 1
            current_file_tokens = 0
            current_file_data = []

    for i, v in enumerate(df["decisao"]):
        item = generate_batch_item(
            id=str(f"{i:04}"),
            model=model,
            prompt=prompt,
            variable=v,
        )

        item_str = json.dumps(item["body"]["messages"])  # type: ignore
        item_tokens = len(item_str)

        if current_file_tokens + item_tokens > max_tokens:
            write_current_file()

        current_file_data.append(item)
        current_file_tokens += item_tokens

    write_current_file()  # Write the remaining items to the last file


def check_batch_cost(model: str, output: str) -> None:
    with open(output, "r", encoding="utf-8") as _file:
        batched = _file.readlines()

        costs = 0
        for item in batched:
            js = json.loads(item.strip())
            content = str(js["body"]["messages"])
            costs += estimate_batch_costs(model, content)
        print(f"Cost Estimation: just the input will cost ${costs:.2f} USD")


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
    generate_batch(df, BATCH_FILE, AI_MODEL, PROMPT, BATCH_SIZE_LIMIT)
    check_batch_cost(AI_MODEL, BATCH_FILE)  # TODO
    print("batch prepared at ", BATCH_FILE)


if __name__ == "__main__":
    main()
