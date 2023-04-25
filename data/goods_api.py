from flask import Blueprint, jsonify, request
from . import db_session
from .goods import Goods

api = Blueprint('goods_api', __name__, template_folder='templates')

db_session.global_init('db/data.db')
session = db_session.create_session()


@api.route('/api/goods')
def get_goods():
    goods_list = session.query(Goods).all()
    return jsonify({'goods': [i.to_dict(only=('name', 'desc', 'price')) for i in goods_list]})


@api.route('/api/goods/<int:id_>', methods={'GET'})
def get_one_goods(id_):
    goods = session.get(Goods, id_)
    if not goods:
        return jsonify({'error': 'Not found'})
    return jsonify({'goods': goods.to_dict(only=('name', 'desc', 'price'))})


@api.route('/api/goods', methods={'POST'})
def create_goods():
    if not request.json:
        return jsonify({'error': 'Empty request'})
    if not all(key in request.json for key in {'name', 'desc', 'price', 'image'}):
        return jsonify({'error': 'Bad request'})
    goods = Goods(
        name=request.json['name'],
        desc=request.json['desc'],
        price=request.json['price'],
        image=request.json['image']
    )
    session.add(goods)
    session.commit()
    return jsonify({'success': 'OK'})


@api.route('/api/goods/<int:id_>', methods={'DELETE'})
def delete_goods(id_):
    goods = session.get(Goods, id_)
    if not goods:
        return jsonify({'error': 'Not found'})
    session.delete(goods)
    session.commit()
    return jsonify({'success': 'OK'})
