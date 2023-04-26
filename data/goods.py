import sqlalchemy as sa
from sqlalchemy import orm
from sqlalchemy_serializer import SerializerMixin
from .db_session import SqlAlchemyBase

association_table = sa.Table(
    'association_order_goods',
    SqlAlchemyBase.metadata,
    sa.Column('orders', sa.Integer, sa.ForeignKey('orders.id')),
    sa.Column('goods_list', sa.Integer, sa.ForeignKey('goods.id'))
)


class Goods(SqlAlchemyBase, SerializerMixin):
    __tablename__ = 'goods'
    id = sa.Column(sa.Integer, primary_key=True, autoincrement=True)
    name = sa.Column(sa.String, unique=True, nullable=True)
    desc = sa.Column(sa.Text, nullable=True)
    price = sa.Column(sa.Double, nullable=True)
    image = sa.Column(sa.String, nullable=True)
    categories = orm.relationship('Category', secondary='association_category_goods', backref='goods')
