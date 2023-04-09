import datetime as dt
import sqlalchemy as sa
from sqlalchemy import orm
from .db_session import SqlAlchemyBase


class Order(SqlAlchemyBase):
    __tablename__ = 'order'
    id = sa.Column(sa.Integer, primary_key=True, autoincrement=True)
    user_id = sa.Column(sa.Integer, sa.ForeignKey('users.id'))
    goods = sa.Column(sa.String, nullable=True)
    delivery_date = sa.Column(sa.Date, default=dt.datetime.now().date())
    user = orm.relationship('User')
