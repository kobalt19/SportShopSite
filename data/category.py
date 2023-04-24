import sqlalchemy as sa
from sqlalchemy import orm
from .db_session import SqlAlchemyBase

association_table = sa.Table(
    'association_category_goods',
    SqlAlchemyBase.metadata,
    sa.Column('category', sa.Integer, sa.ForeignKey('category.id')),
    sa.Column('goods', sa.Integer, sa.ForeignKey('goods.id'))
)


class Category(SqlAlchemyBase):
    __tablename__ = 'category'
    id = sa.Column(sa.Integer, primary_key=True, autoincrement=True)
    name = sa.Column(sa.String, unique=True)
