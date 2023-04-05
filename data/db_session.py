import sqlalchemy as sa
from sqlalchemy import orm
from sqlalchemy.orm import Session
import sqlalchemy.ext.declarative as dec

SqlAlchemyBase = dec.declarative_base()
__factory = None


def global_init(db_file):
    global __factory
    if __factory:
        return
    if not db_file.strip():
        raise SystemExit('Необходимо указать файл базы данных.')
    conn_str = f'sqlite:///{db_file.strip()}?check_same_thread=False'
    print(f'Подключение к базе данных по адресу {conn_str}')
    engine = sa.create_engine(conn_str, echo=False)
    __factory = orm.sessionmaker(bind=engine)
    from . import __all_models
    SqlAlchemyBase.metadata.create_all(engine)


def create_session() -> Session:
    return __factory()