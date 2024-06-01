import tiktoken

OMNI_INPUT = 5
OMNI_OUTPUT = 15


def estimate_costs(model: str, n_tokens: int) -> None:
    if model == "gpt-4o":
        MODEL_INPUT = OMNI_INPUT / 1_000_000
        MODEL_OUTPUT = OMNI_OUTPUT / 1_000_000
    else:
        raise ValueError("Model not supported.")

    input_cost = n_tokens * MODEL_INPUT
    output_cost = n_tokens * MODEL_OUTPUT
    total_cost = input_cost + output_cost

    print("Antiquarian AI Cleanup Cost Estimation:")
    print("Model: ", model)
    print(f"Tokens: {n_tokens} + {n_tokens}")
    print(f"Total Estimated Cost: ${total_cost:.2f}")


def get_costs_gpt4o(response) -> None:
    MODEL_INPUT = OMNI_INPUT / 1_000_000
    MODEL_OUTPUT = OMNI_OUTPUT / 1_000_000

    print("\nActual Cost: ")
    i_tokens = response.usage.prompt_tokens
    o_tokens = response.usage.completion_tokens
    print(f"Tokens: {i_tokens} + {o_tokens}")

    input_cost = i_tokens * MODEL_INPUT
    output_cost = o_tokens * MODEL_OUTPUT
    total_cost = input_cost + output_cost

    print(f"Cost: {input_cost:.4f} + {output_cost:.4f}")
    print(f"Total Cost: ${total_cost:.2f}")


def get_n_tokens(model: str, text: str) -> int:
    encoding = tiktoken.encoding_for_model(model)
    tokenized = encoding.encode(text)
    n_tokens = len(tokenized)
    return n_tokens
