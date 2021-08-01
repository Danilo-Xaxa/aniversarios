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


global EMAIL_REMETENTE, EMAIL_SENHA
EMAIL_REMETENTE = getenv('EMAIL_REMETENTE')
EMAIL_SENHA = getenv('EMAIL_SENHA')


@app.route("/", methods=["GET", "POST"])
def index():
    global servidor_smtp
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
        session['aniversariantes'] = []
        session['emails'] = []

        for counter, row in enumerate(rows):
            day, month = str(row["day"]), str(row["month"])

            day = day if len(day) == 2 else '0' + day
            month = month if len(month) == 2 else '0' + month

            niver = f'{day}/{month}'
            hoje = datetime.now(timezone('America/Recife')).strftime("%d/%m")

            if niver == hoje:
                textos.append(f'Hoje é o aniversário de {row["name"]}!')
                emails.append(row["email"])
                session['aniversariantes'].append(row["name"])
                session['emails'].append(row["email"])

                if counter == len(rows) - 1:  # fazer só na última vez
                    servidor_smtp = SMTP("smtp.gmail.com", 587)
                    servidor_smtp.starttls()
                    servidor_smtp.login(EMAIL_REMETENTE, EMAIL_SENHA)

        return render_template("index.html", rows=rows, textos=textos, aniversariantes=session['aniversariantes'])

@app.route("/email_parabens", methods=["GET", "POST"])
def email_parabens():
    if request.method == 'GET':
        indice = int(request.args.get('aniversariante'))
        session['aniversariante'] = session.get('aniversariantes')[indice]
        session['email'] = session.get('emails')[indice]
        return render_template('email_parabens.html')

    elif request.method == 'POST':
        if request.form.get('padrao') == 'Enviar e-mail padrão':
            desejou = request.form.get('name')
            assunto = "Feliz aniversário!"
            mensagem = f"Parabéns, {session['aniversariante']}! {desejou.strip().capitalize()} te desejou um feliz aniversário :)"
            assunto_mensagem = (f"Subject: {assunto}\n\n{mensagem}")
            servidor_smtp.sendmail(EMAIL_REMETENTE, session['email'], assunto_mensagem.encode("utf8"))

            return render_template('enviado.html', mensagem=mensagem)

        elif request.form.get('personalizado') == 'Enviar e-mail personalizado':
            session['desejou'] = request.form.get('name')
            return redirect('/personalizado')

@app.route("/personalizado", methods=["GET", "POST"])
def personalizado():
    if request.method == 'GET':
        return render_template('personalizado.html')

    elif request.method == 'POST':
        mensagem = request.form.get('msg_personalizada')
        desejou = session['desejou']
        assunto = f"{desejou} te enviou este e-mail: "
        assunto_mensagem = (f"Subject: {assunto}\n\n{mensagem}")
        servidor_smtp.sendmail(EMAIL_REMETENTE, session['email'], assunto_mensagem.encode("utf8"))

        return render_template('enviado.html', mensagem=assunto+mensagem)
