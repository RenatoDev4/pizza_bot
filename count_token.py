import tiktoken


def count_tokens(prompt):
    encoder = tiktoken.encoding_for_model("gpt-3.5-turbo")
    tokens_list = encoder.encode(prompt)
    count = len(tokens_list)
    return count


def historic_limit(historic, max_limit_tokens):
    total_tokens = 0
    parcial_historic = ""
    for line in reversed(historic.split("\n")):
        line_tokens = count_tokens(line)
        total_tokens = total_tokens + line_tokens
        if total_tokens > max_limit_tokens:
            break
        parcial_historic = line + parcial_historic
    return parcial_historic
