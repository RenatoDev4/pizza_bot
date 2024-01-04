import os

from dotenv import load_dotenv
from openai import OpenAI

from count_token import count_tokens
from load_save_file import load_info

load_dotenv()
client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))

data_store = load_info("store_data.txt")


def bot(prompt, historic):
    maxima_repeticao = 1
    repeticao = 0
    while True:
        try:
            model = "gpt-3.5-turbo"
            prompt_do_sistema = f"""
            You are a customer service chatbot for a pizza restaurant. \
            You first greet the customer, ask if the costumer want see the menu \
            then collects the order, \
            and then asks if it's a pickup or delivery. \
            You wait to collect the entire order, then summarize it and check for a final \
            time if the customer wants to add anything else. \
            Finally you collect the payment.\
            If it's a delivery, you ask for an address. \
            Make sure to clarify all options, extras and sizes to uniquely \
            identify the item from the menu.\
            You respond in a short, very conversational friendly style. \
            ## Dados do ecommerce:
            {data_store}
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
