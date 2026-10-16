from datetime import date, datetime

from flask import Flask, abort, flash, redirect, render_template, request, url_for

import database as db

app = Flask(__name__)
app.secret_key = "troque-esta-chave-em-producao"

db.init_db()


@app.route("/")
def index():
    return render_template("index.html", signos=db.listar_signos(), hoje=date.today().isoformat())


@app.post("/descobrir")
def descobrir():
    """Recebe a data, identifica o signo no BD e redireciona para a página do signo."""
    texto = request.form.get("data_nascimento", "").strip()
    try:
        nasc = datetime.strptime(texto, "%Y-%m-%d").date()
    except ValueError:
        flash("Informe uma data de nascimento válida.", "danger")
        return redirect(url_for("index"))

    if nasc > date.today() or nasc.year < 1900:
        flash("A data deve estar entre 1900 e hoje.", "danger")
        return redirect(url_for("index"))

    signo = db.buscar_signo_por_data(nasc.month, nasc.day)
    db.registrar_consulta(nasc.isoformat(), signo["id"])
    return redirect(url_for("signo", slug=signo["slug"], nasc=nasc.strftime("%d/%m/%Y")))


@app.route("/signo/<slug>")
def signo(slug):
    s = db.buscar_signo_por_slug(slug)
    if s is None:
        abort(404)
    return render_template("signo.html", s=s, nasc=request.args.get("nasc"))


@app.errorhandler(404)
def nao_encontrado(_):
    return render_template("404.html"), 404


if __name__ == "__main__":
    app.run(debug=True)
