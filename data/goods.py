import sqlalchemy as sa
from .db_session import SqlAlchemyBase
from utils.utils import get_pic_by_id

association_table = sa.Table(
    'association_order_goods',
    SqlAlchemyBase.metadata,
    sa.Column('orders', sa.Integer, sa.ForeignKey('orders.id')),
    sa.Column('goods_list', sa.Integer, sa.ForeignKey('goods.id'))
)


class Goods(SqlAlchemyBase):
    __tablename__ = 'goods'
    id = sa.Column(sa.Integer, primary_key=True, autoincrement=True)
    name = sa.Column(sa.String, unique=True, nullable=True)
    desc = sa.Column(sa.Text, nullable=True)
    category = sa.Column(sa.String, nullable=True)
    price = sa.Column(sa.Double, nullable=True)
    image = sa.Column(sa.String, nullable=True)

    def set_image(self):
        self.image = get_pic_by_id(self.id)
