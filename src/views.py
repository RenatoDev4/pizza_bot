import os
from typing import Dict

from flask import (Flask, Response, flash, redirect, render_template, request,
                   session, url_for)

from src.func_bot import treat_response
from src.load_save_file import load_info
from src.models import User

app = Flask(__name__, template_folder="../templates", static_folder="../static")
app.secret_key = "chat_bot"
usuarios: Dict[str, User] = {}


@app.route("/")
def home() -> str:
    """
    Renders the home page if a user is logged in, otherwise redirects to the login page.

    Returns:
        str: The HTML content of the home page or a redirect to the login page.
    """
    if "usuario_logado" not in session or session["usuario_logado"] == None:
        return redirect(url_for("login"))
    return render_template("index.html")


@app.route("/chat", methods=["POST"])
def chat() -> Response:
    """
    Handles the chat functionality by processing incoming messages.

    Args:
        None (uses Flask's request and session objects)

    Returns:
        Response: The response containing processed chat information.

    Raises:
        None
    """
    prompt: str = request.json["msg"]
    file_name: str = session["usuario_logado"]
    historic: str = ""

    if os.path.exists(file_name):
        historic = load_info(file_name)

    return Response(
        treat_response(prompt, historic, file_name), mimetype="text/event-stream"
    )


@app.route("/limparhistorico", methods=["POST"])
def clean_historic() -> Dict:
    """
    Clears the user's historical data.

    This function is associated with the "/limparhistorico" route and is triggered
    via a POST request. It retrieves the current user's session and removes the
    corresponding historical data file. The response is an empty dictionary.

    Returns:
        Dict: An empty dictionary as the response.

    Example:
        After making a POST request to "/limparhistorico", the user's historical
        data file is deleted, and the server responds with an empty dictionary.

    """
    file_name = session["usuario_logado"]
    if os.path.exists(file_name):
        os.remove(file_name)
    return {}


@app.route("/registrar", methods=["POST"])
def registrar() -> str:
    """
    Registers a new user based on the provided form data.

    Returns:
    - str: A redirect to the login page.

    Raises:
    - Flash: If the username is less than 3 characters.
    - Flash: If the username is already in use.
    """
    name: str = request.form["name"]
    nickname: str = request.form["nickname"]

    if len(nickname) < 3:
        flash("Nome de usuário deve ter pelo menos 3 caracteres")
        return redirect(url_for("login"))

    if nickname in usuarios:
        flash("Nome de usuário já em uso. Escolha outro.")
        return redirect(url_for("login"))

    novo_usuario = User.create_user(name, nickname)
    usuarios[nickname] = novo_usuario

    flash("Usuário registrado com sucesso! Faça o login.")
    return redirect(url_for("login"))


@app.route("/login")
def login() -> str:
    """
    Renders the login.html template for the "/login" route.

    Returns:
    - str: Rendered HTML content for the login page.

    Example:
    ```
    @app.route("/login")
    def login():
        return render_template("login.html", proxima="/")
    ```
    """
    return render_template("login.html", proxima="/")


@app.route(
    "/autenticar",
    methods=[
        "POST",
    ],
)
def autenticar() -> str:
    """
    Authenticate user based on the provided credentials.

    This function handles the authentication process for a user attempting
    to log in. It checks if the provided username exists in the 'usuarios'
    dictionary. If found, it logs in the user, sets the session variable
    'usuario_logado', and redirects to the next page. If the username does
    not exist, it displays an error message and redirects to the login page.

    Returns:
    - If authentication is successful, redirects to the next page.
    - If the username does not exist, redirects to the login page.

    """
    if request.form["usuario"] in usuarios:
        usuario = usuarios[request.form["usuario"]]
        session["usuario_logado"] = usuario.nickname
        flash(usuario.nickname + " logado com sucesso!")
        return redirect(request.form["proxima"])
    else:
        flash("Usuário não existe, por favor registre um novo.")
        return redirect(url_for("login"))


@app.route("/logout")
def logout():
    file_name = session["usuario_logado"]

    if os.path.exists(file_name):
        os.remove(file_name)

    session["usuario_logado"] = None
    flash("Logout efetuado com sucesso!")
    return redirect(url_for("login"))
