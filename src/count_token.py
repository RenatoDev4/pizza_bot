import tiktoken


def count_tokens(prompt: str) -> int:
    """
    Count the number of tokens in a prompt.
    Args:
        prompt (str): The prompt to count tokens for.
    Returns:
        int: The number of tokens in the prompt.
    """
    encoder = tiktoken.encoding_for_model("gpt-3.5-turbo")
    tokens_list = encoder.encode(prompt)
    count = len(tokens_list)
    return count


def historic_limit(historic: str, max_limit_tokens: int) -> str:
    """
    Calculate the partial historic by considering a maximum limit of tokens.

    Args:
        historic (str): The entire historic string.
        max_limit_tokens (int): The maximum limit of tokens.

    Returns:
        str: The partial historic string within the token limit.
    """
    total_tokens = 0
    parcial_historic = ""
    for line in reversed(historic.split("\n")):
        line_tokens = count_tokens(line)
        total_tokens = total_tokens + line_tokens
        if total_tokens > max_limit_tokens:
            break
        parcial_historic = line + parcial_historic
    return parcial_historic
