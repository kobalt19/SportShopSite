import datetime as dt
from flask import abort, Flask, jsonify, render_template, redirect, request, session
from flask_login import AnonymousUserMixin, current_user, LoginManager, login_required, login_user, logout_user, \
    UserMixin
from data import db_session, goods_api
from data.category import Category
from data.goods import Goods
from data.order import Order
from data.users import User
from forms.goods import GoodsForm
from forms.order import OrderForm
from forms.user import LoginForm, RegisterForm
import sqlalchemy as sa
import sqlalchemy.exc

app = Flask(__name__)
app.register_blueprint(goods_api.api)
app.config['SECRET_KEY'] = 'yandexlyceum_secret_key'
app.config['PERMANENT_SESSION_LIFETIME'] = dt.timedelta(days=365)

login_manager = LoginManager()
login_manager.init_app(app)

db_session.global_init('db/data.db')
db_sess = db_session.create_session()


@login_manager.user_loader
def load_user(user_id):
    return db_sess.get(User, user_id)


@app.errorhandler(401)
def unauthorized(err):
    return render_template('error.html', message='У вас нет права на доступ к этой странице!')


@app.route('/register/', methods={'GET', 'POST'})
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        if form.password.data != form.password_again.data:
            return render_template('register.html', title='Регистрация', form=form, message='Пароли не совпадают')
        if db_sess.query(User).filter(User.email == form.email.data).first():
            return render_template('register.html', title='Регистрация', form=form,
                                   message='Такой пользователь уже есть')
        user = User(
            surname=form.surname.data,
            name=form.name.data,
            email=form.email.data,
        )
        user.set_password(form.password.data)
        db_sess.add(user)
        db_sess.commit()
        return redirect('/login')
    return render_template('register.html', title='Регистрация', form=form)


@app.route('/login/', methods={'GET', 'POST'})
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = db_sess.query(User).filter(User.email == form.email.data).first()
        if user and user.check_password(form.password.data):
            login_user(user, remember=form.remember_me.data)
            return redirect('/')
        return render_template('login.html', message='Неправильный логин или пароль', form=form)
    return render_template('login.html', title='Авторизация', form=form)


@app.route('/logout/')
@login_required
def logout():
    logout_user()
    return redirect('/')


@app.route('/add_goods/', methods={'GET', 'POST'})
@login_required
def add_goods():
    form = GoodsForm()
    if not current_user.is_authenticated or current_user.id != 1:
        return unauthorized()
    if form.validate_on_submit():
        category_name = form.category.data
        category = db_sess.query(Category).filter(Category.name == category_name).first()
        if not category:
            category = Category(name=category_name)
            db_sess.add(category)
            db_sess.commit()
        new_goods = Goods(
            name=form.name.data,
            desc=form.description.data,
            price=form.price.data,
        )
        new_goods.categories.append(category)
        try:
            db_sess.add(new_goods)
            db_sess.commit()
            new_goods.set_image()
            db_sess.commit()
        except sa.exc.IntegrityError:
            return render_template('error.html', message='Товар с таким именем уже есть в базе данных!')
        return redirect('/')
    return render_template('add_goods.html', title='Добавление товара', form=form)


@app.route('/goods/<int:id_>')
def goods(id_):
    found_goods = db_sess.get(Goods, id_)
    if not found_goods:
        return render_template('error.html', message='Товара с данным id не существует!')
    return render_template('goods.html', goods=found_goods)


@app.route('/catalogue/')
def catalogue():
    categories = {category.name: category.goods for category in db_sess.query(Category).all()}
    kwargs = {
        'title': 'Каталог',
        'catalogue': categories,
    }
    return render_template('catalogue.html', **kwargs)


@app.route('/add_to_order/<int:id_>', methods={'GET', 'POST'})
def add_to_order(id_):
    if not current_user.is_authenticated:
        return render_template('error.html', message='Сначала войдите в свой аккаунт!')
    current_order = None
    if 'current_order' in session:
        current_order = db_sess.get(Order, session['current_order'])
    if not current_order:
        current_order = db_sess.query(Order).filter(Order.user_id == current_user.id).first()
        if current_order:
            session['current_order'] = current_order.id
        else:
            order_ = Order(user_id=current_user.id)
            db_sess.add(order_)
            db_sess.commit()
            session['current_order'] = order_.id
            current_order = order_
    goods_ = db_sess.get(Goods, id_)
    if not goods_:
        return render_template('error.html', message='Товар по указанному id не найден!')
    current_order.goods_list.append(goods_)
    db_sess.commit()
    return redirect('/order')


@app.route('/remove_from_order/<int:id_>', methods={'GET', 'POST'})
def remove_from_order(id_):
    if 'current_order' not in session:
        return render_template('error.html', message='У вас нет активной корзины!')
    current_order = db_sess.get(Order, session['current_order'])
    if not current_order:
        return render_template('error.html', message='Не найдена активная корзина!')
    goods_ = db_sess.get(Goods, id_)
    if not goods_:
        return render_template('error.html', message='Товар по указанному id не найден!')
    try:
        current_order.goods_list.remove(goods_)
    except BaseException as err:
        print(err.__class__.__name__, err)
    db_sess.commit()
    return redirect('/order/')


@app.route('/order/', methods={'GET', 'POST'})
def order():
    form = OrderForm()
    try:
        current_order = db_sess.get(Order, session['current_order'])
        assert current_order
    except (KeyError, AssertionError):
        current_order = db_sess.query(Order).filter(Order.user_id == current_user.id).first()
        if current_order and not current_order.completed:
            session['current_order'] = current_order.id
        else:
            order_ = Order(user_id=current_user.id, goods='')
            db_sess.add(order_)
            db_sess.commit()
            session['current_order'] = order_.id
            current_order = order_
    if form.validate_on_submit():
        if current_order.completed:
            abort(500)
        current_order.delivery_date = form.date.data
        current_order.completed = True
        current_user.orders_list.append(current_order)
        db_sess.commit()
        return redirect('/order/success/')
    goods_list = sorted(current_order.goods_list, key=lambda goods_: goods_.name)
    total_price = sum(goods_.price for goods_ in goods_list)
    kwargs = {
        'order': current_order,
        'goods_list': goods_list,
        'total_price': total_price,
        'form': form,
    }
    if current_user.id == 1:
        print(current_order.id)
    return render_template('order.html', **kwargs)


@app.route('/order/<int:id_>')
def show_order(id_):
    order_ = db_sess.get(Order, id_)
    if not order_:
        return render_template('error.html', message='Заказ с указанным id не найден!')
    goods_list = sorted(order_.goods_list, key=lambda goods_: goods_.name)
    total_price = sum(goods_.price for goods_ in goods_list)
    kwargs = {
        'order': order_,
        'goods_list': goods_list,
        'total_price': total_price,
        'form': None,
    }
    return render_template('order.html', **kwargs)


@app.route('/order/success/')
def successful_order():
    return render_template('succesful_order.html', title='Заказ оформлен!')


@app.route('/user/<int:id_>')
def user_page(id_):
    if not current_user.is_authenticated or id_ not in {1, current_user.id}:
        return render_template('error.html', message='У вас нет права просматривать страницу данного пользователя!')
    user = db_sess.get(User, id_)
    if not user:
        return render_template('error.html', message='Пользователь с данным id не найден!')
    kwargs = {
        'user': user,
        'costs': (sum(goods_.price for goods_ in order_.goods_list) for order_ in user.orders_list),
        'next': next,
    }
    return render_template('user.html', **kwargs)


@app.route('/')
def index():
    kwargs = {
        'title': 'SportShopSite',
    }
    return render_template('index.html', **kwargs)


def main():
    app.run(host='127.0.0.1', port=8080)


if __name__ == '__main__':
    main()
