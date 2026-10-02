from sqlalchemy import select

from database import Partida, db_session


def select_todos_tabela():
    #Buscar todos os times no banco
    # 1- Montar o select
    partidas_sql = select(Partida)
    # 2- Executar o select
    times = db_session.execute(partidas_sql).scalars().all()
    return times

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