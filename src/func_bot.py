import os
from typing import Generator

from dotenv import load_dotenv
from openai import OpenAI

from src.count_token import count_tokens, historic_limit
from src.load_save_file import load_info, save

load_dotenv()
client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))

data_store = load_info("src/store/store_data.txt")


def treat_response(
    prompt: str, historic: str, file_name: str
) -> Generator[str, None, None]:
    """
    Generate a response to the given prompt, save the response to a file,
    and yield each response piece.

    Args:
        prompt: The user prompt to generate a response to.
        historic: The historic conversation to provide context for the response.
        file_name: The name of the file to save the response to.

    Yields:
        Each response piece.

    """
    partial_answer = ""
    max_limit_tokens = 1500
    parcial_historic = historic_limit(historic, max_limit_tokens)
    for resposta in bot(prompt, parcial_historic):
        response_piece = getattr(resposta.choices[0].delta, "content", "")  # type: ignore
        if response_piece is not None and len(response_piece):
            partial_answer += response_piece
            yield response_piece
    content = f"""
    Historic: {parcial_historic}
    User: {prompt}
    IA: {partial_answer}
    """
    save(file_name, content)


def bot(prompt: str, historic: str) -> str:
    """
    Generates a comment for the given function body in a markdown code block with the correct language syntax.

    Args:
        prompt (str): The prompt to be used for generating the function comment.
        historic (str): The historic data to be included in the function comment.

    Returns:
        str: The generated function comment in markdown format.
    """
    maxima_repeticao = 1
    repeticao = 0
    while True:
        try:
            model = "gpt-3.5-turbo"
            prompt_do_sistema = f"""
            # CONTEXT #
            You are a customer service chatbot for a pizza restaurant. \
            If you are asked something out of context, answer: \
            Sou um robô programado para fornecer respostas exclusivamente relacionadas ao estabelecimento que me contratou. \

            #############

            # OBJECTIVE #
            You first greet the customer, ask if the costumer want see the menu \
            then collects the order, \
            and then asks if it's a pickup or delivery. \
            You wait to collect the entire order, then summarize it and check for a final. \
            time if the customer wants to add anything else. \
            Finally you collect the payment, you must only accept the PIX payment method.\
            If it's a delivery, you ask for an address. \
            Make sure to clarify all options, extras and sizes to uniquely. \
            Be sure to calculate the value of all products and inform the customer after he confirms the products. \
            identify the item from the menu.\
            You respond in a short, very conversational friendly style. \

            #############

            ## Dados do ecommerce:
            {data_store}

            #############

            ## Historico:
            {historic}

            \n
            """
            expected_output_size = 2000
            total_tokens_model = 4000
            if (
                count_tokens(prompt_do_sistema)
                >= total_tokens_model - expected_output_size
            ):
                model = "gpt-3.5-turbo-16k"
            conversation = [
                {"role": "system", "content": prompt_do_sistema},
                {"role": "user", "content": prompt},
            ]
            response = client.chat.completions.create(
                model=model,
                messages=conversation,
                temperature=0,
                max_tokens=400,
                top_p=1,
                frequency_penalty=0,
                presence_penalty=0,
                stream=True,
            )
            return response
        except Exception as erro:
            repeticao += 1
            if repeticao >= maxima_repeticao:
                return "Erro de resposta do modelo: %s" % erro
            print("Erro de comunicação com OpenAI:", erro)
