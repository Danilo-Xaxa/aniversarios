from cs50 import SQL
from flask import Flask, redirect, render_template, flash, session, request
from flask_session import Session
from smtplib import SMTP
from datetime import datetime
from pytz import timezone
from os import getenv


# Configure application
app = Flask(__name__)

# Ensure templates are auto-reloaded and configuring the session
app.config["TEMPLATES_AUTO_RELOAD"] = True
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///birthdays.db")

# Setting a random secret key
app.secret_key = b'_5#y2L"2dn399q3bfjkbqk23ie3imdd3'


@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        name = request.form.get("name")
        email = request.form.get("email")
        month = request.form.get("month")
        day = request.form.get("day")

        for chave, valor in {'Nome': name, 'E-mail': email, 'Mês': month, 'Dia': day}.items():
            if not valor:
                return render_template('erro.html', erro=f"{chave} não digitado!")
        
        if int(month) in [4, 6, 9, 11] and int(day) == 31:
            return render_template('erro.html', erro="O mês digitado não tem dia 31!")

        if int(month) == 2 and int(day) > 29:
            return render_template('erro.html', erro=f"Fevereiro não tem dia {int(day)}!")

        name = name.strip().capitalize().split()[0]
        email = email.strip()

        db.execute("INSERT INTO birthdays (name, email, month, day) VALUES (?, ?, ?, ?)", name, email, month, day)

        flash(f'Aniversário de {name} adicionado!')

        return redirect("/")

    elif request.method == "GET":
        rows = db.execute("SELECT * FROM birthdays")
        textos, emails = [], []

        for row in rows:
            day, month = str(row["day"]), str(row["month"])

            day = day if len(day) == 2 else '0' + day
            month = month if len(month) == 2 else '0' + month

            niver = f'{day}/{month}'
            hoje = datetime.now(timezone('America/Recife')).strftime("%d/%m")

            if niver == hoje:
                textos.append(f'Hoje é o aniversário de {row["name"]}!')
                emails.append(row["email"])
                session['aniversariante'] = row["name"]
                session['email'] = row["email"]

        return render_template("index.html", rows=rows, textos=textos, emails=emails)

@app.route("/email_parabens", methods=["GET", "POST"])
def email_parabens():
    aniversariante = session.get('aniversariante')
    email = session.get('email')

    if request.method == 'GET':
        return render_template('email_parabens.html')

    elif request.method == 'POST':
        print('DAQUI PRA BAIXO NÃO FUNFA GRRRRRRRRRRRR')
        if request.form['botao'] == 'Enviar e-mail padrão':
            desejou = request.form.get('name')
            mensagem = f'Parabéns, {aniversariante}! {desejou.strip().capitalize()} te desejou um feliz aniversário :)'

            EMAIL_REMETENTE = getenv('EMAIL_REMETENTE')
            EMAIL_SENHA = getenv('EMAIL_SENHA')

            servidor = SMTP("smtp.gmail.com", 587)
            servidor.starttls()
            servidor.login(EMAIL_REMETENTE, EMAIL_SENHA)
            servidor.sendmail(EMAIL_REMETENTE, email, mensagem.encode("utf8"))

            return render_template('enviado.html', mensagem=mensagem)

        elif request.form['botao'] == 'Enviar e-mail personalizado':
            return redirect('/personalizado')

@app.route("/personalizado", methods=["GET", "POST"])
def personalizado():
    if request.method == 'GET':
        return render_template('personalizado.html')

    elif request.method == 'POST':
        pass
