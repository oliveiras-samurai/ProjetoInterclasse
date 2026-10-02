from os import times

from flask import Flask, render_template, request, redirect, url_for, flash, g
from sqlalchemy import select
from sqlalchemy.exc import SQLAlchemyError

from banco import tabela_time, tabela_jogador, tabela_partida
from database import *

app = Flask(__name__)
app.secret_key = "chave-secreta-interclasse-2026"


@app.route("/")
def dashboard():
    times_sql = select(Time)
    jogadores_sql = select(Jogador)
    partidas_sql = select(Partida)
    # 2- Executar o select
    times = db_session.execute(times_sql).scalars().all()
    jogadores = db_session.execute(jogadores_sql).scalars().all()
    partidas = db_session.execute(partidas_sql).scalars().all()
    return render_template(
        "dashboard.html",
        total_jogadores=len(jogadores),
        total_times=len(times),
        total_partidas=len(partidas),
    )


@app.route("/jogadores")
def listar_jogadores():
    #buscar jogadores no banco
    jogadores_sql = select(Jogador)
    # 2- Executar o select
    jogadores = db_session.execute(jogadores_sql).scalars().all()
    return render_template("jogadores.html", jogadores=jogadores, times=[])


@app.route("/jogadores/novo", methods=["GET", "POST"])
def novo_jogador():

    # Quando clicar no botão de cadastrar
    if request.method == "POST":
        nome = request.form.get("nome").strip()
        numero_camisa = request.form.get("numero_camisa") or None
        posicao = request.form.get("posicao").strip()
        time_id = request.form.get("time_id") or None
        #verificar se foi digitado
        if not nome:
            flash('Preencha o Nome', 'error')
            return redirect(url_for("novo_jogador"))
        if not numero_camisa:
            flash('Preencha o Numero da Camisa', 'error')
            return redirect(url_for("jogadores.html"))
        if not posicao:
            flash('Preencha a Posição', 'error')
            return redirect(url_for("jogadores.html"))
        if not time_id:
            flash('Preencha o Time', 'error')
            return redirect(url_for("jogadores.html"))
        # Salvar no banco
        tabela_jogador.salvar(nome=nome, numero_camisa=numero_camisa, posicao=posicao, time_id=time_id)

    jogadores = (tabela_jogador.select_todos())
    return render_template("jogadores.html", jogadores=jogadores, times=times)

@app.route("/jogadores/excluir/<jogador_id>", methods=["GET", "POST"])
def excluir_jogador(jogador_id):
    print(jogador_id)
    jogador_sql = select(Jogador).where(jogador_id)

@app.route("/times")
def listar_times():
    times_sql = select(Time)
    # 2- Executar o select
    times = db_session.execute(times_sql).scalars().all()
    return render_template("times.html", times=times)



@app.route("/times/novo", methods=["GET", "POST"])
def time_novo():

    if request.method == "POST":
        # 1- Pegaros valores digitados no form
        nome = request.form.get("nome", "").strip()
        turma = request.form.get("turma", "").strip()
        responsavel = request.form.get("responsavel", "").strip()

        # 2- Verificar se foi digitado
        if not nome:
            flash('Preencha o nome', 'error')
            return render_template("times.html", )
        if not turma:
            flash('Preencha a turma', 'error')
            return render_template("times.html", )
        if not responsavel:
            flash('Preencha o nome responsavel', 'error')
            return render_template("times.html", )

        # 3- Salvar no banco
        tabela_time.salvar(nome=nome, turma=turma, responsavel=responsavel)

    times = tabela_time.select_todos()
    return render_template("times.html", times=times)


@app.route("/partidas")
def listar_partidas():
    partidas = tabela_partida.select_todos()
    return render_template("partidas.html", partidas=partidas, times=[])


@app.route("/partidas/nova", methods=["GET", "POST"])
def nova_partida():

    if request.method == "POST":
        # 1- verificar se foi digitado
        time_casa_id = request.form.get("time_casa_id")
        time_visitante_id = request.form.get("time_visitante_id")
        placar_casa = request.form.get("placar_casa") or 0
        placar_visitante = request.form.get("placar_visitante") or 0
        data_partida = request.form.get("data_partida").strip()
        local = request.form.get("local").strip()
        # verificar se foi digitado
        if not time_casa_id:
            flash('Preencha o Time da casa', 'error')
            return render_template("partidas.html")
        if not time_visitante_id:
            flash('Preencha o Time da visitante', 'error')
            return render_template("partidas.html")
        if not placar_casa:
            flash('Preencha o Placar da casa', 'error')
            return render_template("partidas.html")
        if not placar_visitante:
            flash('Preencha o Placar da visitante', 'error')
            return render_template("partidas.html")
        if not data_partida:
            flash('Preencha o Data da partida', 'error')
            return render_template("partidas.html")
        # 3- verificar se os times sao iguais
        if time_casa_id == time_visitante_id:
            flash('Selecione um time diferente', 'error')


        # 4 - Salvar no banco
        tabela_partida.salvar(time_casa_id=time_casa_id, placar_visitante=placar_visitante,)



    return render_template("partidas.html", partidas=partidas, times=times)


if __name__ == "__main__":
    app.run(debug=True)
