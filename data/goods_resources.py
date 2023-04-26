from flask import jsonify
from flask_restful import reqparse, abort, Api, Resource
from . import db_session
from .goods import Goods

db_session.global_init('db/data.db')
session = db_session.create_session()


parser = reqparse.RequestParser()
parser.add_argument('name', required=True)
parser.add_argument('desc', required=True)
parser.add_argument('price', required=True, type=int)


def check_goods(id_):
    goods = session.get(Goods, id_)
    if not goods:
        abort(404, message=f'Goods with id {id_} not found')


class GoodsResource(Resource):
    @staticmethod
    def get(id_):
        check_goods(id_)
        goods = session.get(Goods, id_)
        return jsonify({'goods': goods.to_dict(only=('name', 'desc', 'price'))})

    @staticmethod
    def delete(id_):
        check_goods(id_)
        goods = session.get(Goods, id_)
        session.delete(goods)
        session.commit()
        return jsonify({'success': 'OK'})


class GoodsListResource(Resource):
    @staticmethod
    def get():
        goods_list = session.query(Goods).all()
        return jsonify({'goods': [goods.to_dict(only=('name', 'desc', 'price')) for goods in goods_list]})

    @staticmethod
    def post():
        args = parser.parse_args()
        goods = Goods(name=args['name'], desc=args['desc'], price=args['price'])
        session.add(goods)
        session.commit()
        return jsonify({'success': 'OK'})
