from cs50 import SQL
from flask import Flask, redirect, render_template, request, flash


# Configure application
app = Flask(__name__)

# Ensure templates are auto-reloaded
app.config["TEMPLATES_AUTO_RELOAD"] = True

# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///birthdays.db")

# Secret key
app.secret_key = b'_5#y2L"2dn399q3bfjkbqk23ie3imdd3'


@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        # Add the user's entry into the database
        name = request.form.get("name")
        month = request.form.get("month")
        day = request.form.get("day")

        for chave, valor in {'Nome': name, 'Mês': month, 'Dia': day}.items():
            if not valor:
                return render_template('erro.html', erro=f"{chave} não digitado!")
        
        if int(month) in [4, 6, 9, 11] and int(day) == 31:
            return render_template('erro.html', erro="O mês digitado não tem dia 31!")

        if int(month) == 2 and int(day) > 29:
            return render_template('erro.html', erro=f"Fevereiro não tem dia {int(day)}!")

        name = name.strip().capitalize().split()[0]

        db.execute("INSERT INTO birthdays (name, month, day) VALUES (?, ?, ?)", name, month, day)

        flash(f'Aniversário de {name} adicionado!')

        return redirect("/")

    else:
        # Display the entries in the database on index.html
        rows = db.execute("SELECT * FROM birthdays")

        return render_template("index.html", rows=rows)

@app.route("/email_parabens", methods=["GET", "POST"])
def email_parabens():
    if request.method == 'GET':
        textos, emails = [], []
        rows = db.execute("SELECT * FROM birthdays")  # ta certo?

        for row in rows:  # iterar sobre as rows da db
            if ... == ...:  # data da row == data de hoje
                nome = ...

            texto = f'Hoje é o aniversário de {nome}! Clique aqui para enviar os parabéns.'
            email = ...

            textos.append(texto)
            emails.append(email)

        return render_template('email_parabens.html', textos=textos, emails=emails)
