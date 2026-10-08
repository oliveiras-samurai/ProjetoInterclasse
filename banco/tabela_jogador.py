import time

from flask import flash
from pymysql import times
from sqlalchemy import select
from sqlalchemy.exc import SQLAlchemyError

from database import db_session, Time, Jogador


def select_todos_jogador():
    #Buscar todos os times no banco
    # 1- Montar o select
    #join(tabela que eu quero juntar, condição = chave estrangeira igual chave primaria)
    jogadores_sql = select(Jogador, Time).join(Time, Jogador.time_id == Time.id)
    # 2- Executar o select
    #usar scalars somente quando houver uma tabela
    times = db_session.execute(jogadores_sql).all()
    return times



def salvar_jogador(nome,numero_camisa,posicao,time_id):
    try:
        jogador = Jogador(nome=nome, numero_camisa=int(numero_camisa), posicao=posicao, time_id=int(time_id))
        db_session.add(jogador)
        db_session.commit()
        flash('Jogador criado com sucesso', 'success')
    except SQLAlchemyError as e:
        db_session.rollback()
        flash('Ocorreu um erro, tente novamente', 'error')
        print(f'Erro: {e}')
    except Exception as e:
        db_session.rollback()
        flash('Ocorreu um erro, tente novamente', 'error')
        print(f'Error: {e}')

def select_quantidade_total():
    quantidade_total = db_session.query(Jogador).count()
    return quantidade_total
