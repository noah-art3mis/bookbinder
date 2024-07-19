import os
import json
import pathlib
import tiktoken
import pandas as pd
import numpy as np

# read this
# https://cookbook.openai.com/examples/chat_finetuning_data_prep

METADATA = {"description": "prophet_empty"}
BATCH_FOLDER = "./output/prophet_empty/batches"
FILE_NAME = "book-5_chunked88_withprev_sample500"

INPUT_FILE = f"./input/prophet/{FILE_NAME}.csv"
BASE_MODEL = "gpt-3.5-turbo-0125"
BATCH_SIZE_LIMIT = 80_000_000  # tier 4 org
QUESTION_COLUMN = "previous_sentence"
ANSWER_COLUMN = "content"


def generate_finetune_item(
    model: str, question: str, answer: str, system: str | None = None
) -> object:

    if "gpt-3.5-turbo" in model:
        if system:
            return {
                "messages": [
                    {"role": "system", "content": system},
                    {"role": "user", "content": question},
                    {"role": "assistant", "content": answer},
                ]
            }
        else:
            return {
                "messages": [
                    {"role": "user", "content": question},
                    {"role": "assistant", "content": answer},
                ]
            }
    elif "davinci" in model or "babbage" in model:
        return {"prompt": question, "completion": answer}
    else:
        raise Exception(f"Unsupported model: {model}")


def generate_finetune_batch(
    df: pd.DataFrame,
    question_col: str,
    answer_col: str,
    output_folder: str,
    output_file: str,
    max_tokens: int,
    model: str,
) -> None:

    current_file_index = 0
    current_file_tokens = 0
    current_file_data = []

    def write_current_file():
        nonlocal current_file_index, current_file_tokens, current_file_data

        if current_file_data:

            file_name = f"{output_folder}/{output_file}_{current_file_index:04}.jsonl"

            with open(file_name, "w", encoding="utf-8") as outfile:

                costs = 0
                for index, item in enumerate(current_file_data):
                    result = json.dumps(item)
                    costs += estimate_finetune_costs(model, result)

                    if index == len(current_file_data) - 1:  # last item
                        outfile.write(result)
                    else:
                        outfile.write(result + "\n")
                print(f"Cost Estimation: finetune will cost ${costs:.2f} USD")

            current_file_index += 1
            current_file_tokens = 0
            current_file_data = []

    for question, answer in zip(df[question_col], df[answer_col]):

        if question is None or question is np.nan:
            question = ""

        if answer is None or answer is np.nan:
            answer = ""

        item_tokens = len(question + " " + answer)
        item = generate_finetune_item(model, question, answer)

        if current_file_tokens + item_tokens > max_tokens:
            write_current_file()

        current_file_data.append(item)
        current_file_tokens += item_tokens

    write_current_file()  # Write the remaining items to the last file


def estimate_finetune_costs(model: str, content: str) -> float:
    TURBO_TRAINING = 8 / 1_000_000
    DAVINCI_TRAINING = 6 / 1_000_000
    BABBAGE_TRAINING = 0.4 / 1_000_000

    match model:
        case "gpt-3.5-turbo-0125":
            MODEL_INPUT = TURBO_TRAINING
        case "davinci-002":
            MODEL_INPUT = DAVINCI_TRAINING
        case "babbage-002":
            MODEL_INPUT = BABBAGE_TRAINING
        case _:
            raise ValueError("Model not supported.")

    n_tokens = get_n_tokens(model, content)
    input_cost = n_tokens * MODEL_INPUT

    return input_cost


def get_n_tokens(model: str, text: str) -> int:
    encoding = tiktoken.encoding_for_model(model)
    tokenized = encoding.encode(text)
    n_tokens = len(tokenized)
    return n_tokens


def main():
    generate_finetune_batch(
        df=pd.read_csv(INPUT_FILE),
        question_col=QUESTION_COLUMN,
        answer_col=ANSWER_COLUMN,
        output_folder=BATCH_FOLDER,
        output_file=FILE_NAME,
        model=BASE_MODEL,
        max_tokens=BATCH_SIZE_LIMIT,
    )
    print("batches prepared at ", BATCH_FOLDER)


if __name__ == "__main__":
    main()
