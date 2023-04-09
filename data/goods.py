import sqlalchemy as sa
from .db_session import SqlAlchemyBase


class Goods(SqlAlchemyBase):
    __tablename__ = 'goods'
    id = sa.Column(sa.Integer, primary_key=True, autoincrement=True)
    name = sa.Column(sa.String, unique=True, nullable=True)
    price = sa.Column(sa.Double, nullable=True)
