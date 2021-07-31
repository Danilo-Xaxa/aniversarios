from cs50 import SQL
from flask import Flask, redirect, render_template, flash, request
from datetime import datetime
from pytz import timezone


# Configure application
app = Flask(__name__)

# Ensure templates are auto-reloaded
app.config["TEMPLATES_AUTO_RELOAD"] = True

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
                nome = row["name"]
                email = row["email"]
                texto = f'Hoje é o aniversário de {nome}! Clique aqui para enviar os parabéns.'

                textos.append(texto)
                emails.append(email)

        return render_template("index.html", rows=rows)

@app.route("/email_parabens", methods=["GET", "POST"])
def email_parabens(textos, emails):
    if request.method == 'GET':
        return render_template('email_parabens.html', textos=textos, emails=emails)

    elif request.method == 'POST':
        pass
