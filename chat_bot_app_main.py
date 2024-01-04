import os

from dotenv import load_dotenv

from count_token import historic_limit
from func_bot import bot
from load_save_file import save
from views import *

load_dotenv()

os.environ.get("OPENAI_API_KEY")


def trata_resposta(prompt, historic, file_name):
    resposta_parcial = ""
    max_limit_tokens = 2000
    parcial_historic = historic_limit(historic, max_limit_tokens)
    for resposta in bot(prompt, parcial_historic):
        pedaco_da_resposta = getattr(resposta.choices[0].delta, "content", "")  # type: ignore
        if pedaco_da_resposta is not None and len(pedaco_da_resposta):
            resposta_parcial += pedaco_da_resposta
            yield pedaco_da_resposta
    content = f"""
    Historic: {parcial_historic}
    User: {prompt}
    IA: {resposta_parcial}
    """
    save(file_name, content)


if __name__ == "__main__":
    app.run(debug=True)
