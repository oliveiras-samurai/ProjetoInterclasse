from operator import or_

from flask import flash
from sqlalchemy import select
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import aliased

from database import Partida, db_session, Time


def select_todos_tabela():
    #Buscar todos os times no banco
    # 1- Montar o select

    TimeCasa = aliased(Time)
    TimeVisitante = aliased(Time)

    partidas_sql = (
        select(Partida,TimeCasa, TimeVisitante)
        .join(TimeCasa, Partida.time_casa_id == TimeCasa.id)
        .join(TimeVisitante, Partida.time_visitante_id_id == TimeVisitante.id)
    )
    # 2- Executar o select
    partidas_casa = db_session.execute(partidas_sql).all()
    print("partidas_casa")
    return partidas_casa

def salvar_partida(nome, turma,responsavel):
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

def select_quantidade_total():
    quantidade_total = db_session.query(Partida).count()
    return quantidade_total