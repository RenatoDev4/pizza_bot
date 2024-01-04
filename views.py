import os

from flask import (Flask, Response, flash, redirect, render_template, request,
                   session, url_for)

from chat_bot_app_main import trata_resposta
from load_save_file import load_info
from models import *

app = Flask(__name__)
app.secret_key = "chat_bot"
usuarios = {}


@app.route("/")
def home():
    if "usuario_logado" not in session or session["usuario_logado"] == None:
        return redirect(url_for("login"))
    return render_template("index.html")


@app.route("/chat", methods=["POST"])
def chat():
    prompt = request.json["msg"]
    file_name = session["usuario_logado"]
    historic = ""
    if os.path.exists(file_name):
        historic = load_info(file_name)
    return Response(
        trata_resposta(prompt, historic, file_name), mimetype="text/event-stream"
    )


@app.route("/limparhistorico", methods=["POST"])
def clean_historic():
    file_name = session["usuario_logado"]
    if os.path.exists(file_name):
        os.remove(file_name)
    return {}


@app.route("/registrar", methods=["POST"])
def registrar():
    name = request.form["name"]
    nickname = request.form["nickname"]

    if len(nickname) <3:
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
def login():
    return render_template("login.html", proxima="/")


@app.route(
    "/autenticar",
    methods=[
        "POST",
    ],
)
def autenticar():
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
    session["usuario_logado"] = None
    flash("Logout efetuado com sucesso!")
    return redirect(url_for("login"))
