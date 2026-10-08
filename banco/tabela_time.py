from flask import flash
from sqlalchemy import select, func
from sqlalchemy.exc import SQLAlchemyError

from database import Time, db_session
def select_todos():
    #Buscar todos os times no banco
    # 1- Montar o select
    times_sql = select(Time)
    # 2- Executar o select
    times = db_session.execute(times_sql).scalars().all()
    return times

def select_quantidade_total():
    qntd_total = db_session.query(Time).count()
    return qntd_total

def salvar(nome, turma,responsavel):
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


