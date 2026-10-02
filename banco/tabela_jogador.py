from flask import flash
from sqlalchemy import select
from sqlalchemy.exc import SQLAlchemyError

from database import Jogador, db_session

def select_todos_jogador():
    #Buscar todos os times no banco
    # 1- Montar o select
    jogadores_sql = select(Jogador)
    # 2- Executar o select
    times = db_session.execute(jogadores_sql).scalars().all()
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