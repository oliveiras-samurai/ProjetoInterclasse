import select
from flask import Flask, render_template, request, redirect, url_for, flash, g
from sqlalchemy import select
from sqlalchemy.exc import SQLAlchemyError

from database import *

app = Flask(__name__)
app.secret_key = "chave-secreta-interclasse-2026"


@app.route("/")
def dashboard():
    return render_template(
        "dashboard.html",
        total_jogadores=0,
        total_times=0,
        total_partidas=0,
        proximas_partidas=0,
        times_ranking=0,
    )


@app.route("/jogadores")
def listar_jogadores():
    return render_template("jogadores.html", jogadores=[], times=[])


@app.route("/jogadores/novo", methods=["GET", "POST"])
def novo_jogador():

    if request.method == "POST":
        nome = request.form.get("nome", "").strip()
        idade = request.form.get("idade") or None
        posicao = request.form.get("posicao", "").strip()
        time_id = request.form.get("time_id") or None

        if not nome:
            flash('preencha o nome', 'error')
        if not idade:
            flash('preencha a idade', 'error')
        if not posicao:
            flash('preencha a posição', 'error')
        if not time_id:
            flash('preencha o time_id', 'error')

    return render_template("jogadores.html", jogadores=[], times=[])

@app.route("/times")
def listar_times():
    return render_template("times.html", times=[])


@app.route("/times/novo", methods=["GET", "POST"])
def time_novo():

    if request.method == "POST":
        # 1- Pegaros valores digitados no form
        nome = request.form.get("nome", "").strip()
        turma = request.form.get("cor", "").strip()
        responsavel = request.form.get("responsavel", "").strip()

        # 2- Verificar se foi digitado
        if not nome:
            flash('preencha o nome', 'error')
            return render_template("times.html", )
        if not turma:
            flash('preencha o nome', 'error')
            return render_template("times.html", )
        if not responsavel:
            flash('preencha o nome', 'error')
            return render_template("times.html", )

        # 3- Salvar no banco
        try:
            times_novos = Time(nome=nome, turma=turma, responsavel=responsavel)
            db_session.add(times_novos)
            db_session.commit()
            flash('time criado com sucesso', 'success')
        except SQLAlchemyError as e:
            db_session.rollback()
            flash('Ocorreu um erro, tente novamente', 'error')
            print(f'Erro: {e}')
        except Exception as e:
            db_session.rollback()
            flash('Ocorreu um erro, tente novamente', 'error')
            print(f'Error: {e}')

    #Buscar todos os times no banco
    # 1- Montar o select
    times_sql = select(Time)
    # 2- Executar o select
    times = db_session.execute(times_sql).scalars().all()
    print(times)
    return render_template("times.html", times=times)


@app.route("/partidas")
def listar_partidas():

    return render_template("partidas.html", partidas=[], times=[])


@app.route("/partidas/nova", methods=["GET", "POST"])
def nova_partida():

    if request.method == "POST":
        time_casa_id = request.form.get("time_casa_id")
        time_visitante_id = request.form.get("time_visitante_id")
        placar_casa = request.form.get("placar_casa") or 0
        placar_visitante = request.form.get("placar_visitante") or 0
        data_partida = request.form.get("data_partida", "").strip()
        local = request.form.get("local", "").strip()

    return render_template("partidas.html", partidas=[], times=[])


if __name__ == "__main__":
    app.run(debug=True)
