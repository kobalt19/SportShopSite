import datetime as dt
import sqlalchemy as sa
from sqlalchemy import orm
from .db_session import SqlAlchemyBase

association_table = sa.Table(
    'association_user_orders',
    SqlAlchemyBase.metadata,
    sa.Column('users', sa.Integer, sa.ForeignKey('users.id')),
    sa.Column('orders', sa.Integer, sa.ForeignKey('orders.id'))
)


class Order(SqlAlchemyBase):
    __tablename__ = 'orders'
    id = sa.Column(sa.Integer, primary_key=True, autoincrement=True)
    user_id = sa.Column(sa.Integer, sa.ForeignKey('users.id'))
    delivery_date = sa.Column(sa.Date, default=dt.datetime.now().date())
    completed = sa.Column(sa.Boolean, default=False)
    goods_list = orm.relationship('Goods', secondary='association_order_goods', backref='orders')
