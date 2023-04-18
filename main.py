import datetime as dt
from flask import abort, Flask, jsonify, render_template, redirect, request, session
from flask_login import AnonymousUserMixin, current_user, LoginManager, login_required, login_user, logout_user, UserMixin
from data import db_session
from data.goods import Goods
from data.users import User
from forms.goods import GoodsForm
from forms.user import LoginForm, RegisterForm
import sqlalchemy as sa
import sqlalchemy.exc

app = Flask(__name__)
app.config['SECRET_KEY'] = 'yandexlyceum_secret_key'
app.config['PERMANENT_SESSION_LIFETIME'] = dt.timedelta(days=365)

login_manager = LoginManager()
login_manager.init_app(app)

db_session.global_init('db/sports.db')


@login_manager.user_loader
def load_user(user_id):
    db_sess = db_session.create_session()
    return db_sess.get(User, user_id)


@app.errorhandler(401)
def unauthorized():
    return render_template('error.html', message='У вас нет права на доступ к этой странице!')


@app.route('/register/', methods={'GET', 'POST'})
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        if form.password.data != form.password_again.data:
            return render_template('register.html', title='Регистрация', form=form, message='Пароли не совпадают')
        db_sess = db_session.create_session()
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
        return redirect('/login/')
    return render_template('register.html', title='Регистрация', form=form)


@app.route('/login/', methods={'GET', 'POST'})
def login():
    form = LoginForm()
    if form.validate_on_submit():
        db_sess = db_session.create_session()
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
        db_sess = db_session.create_session()
        new_goods = Goods(
            name=form.name.data,
            category=form.category.data,
            desc=form.description.data,
            price=form.price.data,
        )
        try:
            db_sess.add(new_goods)
            db_sess.commit()
            new_goods.set_image()
            db_sess.commit()
        except sa.exc.IntegrityError:
            return render_template('conflict.html')
        return redirect('/')
    return render_template('add_goods.html', title='Добавление товара', form=form)


@app.route('/goods/<int:id_>')
def goods(id_):
    db_sess = db_session.create_session()
    found_goods = db_sess.get(Goods, id_)
    if not found_goods:
        return render_template('error.html', message='Товара с данным id не существует!')
    return render_template('goods.html', goods=found_goods)


@app.route('/catalogue/')
def catalogue():
    db_sess = db_session.create_session()
    goods_list = db_sess.query(Goods).all()
    categories = {}
    for goods_ in goods_list:
        if goods.category not in categories:
            categories[goods_.category] = [goods_]
        else:
            categories[goods_.category].append(goods_)
    kwargs = {
        'title': 'Каталог',
        'catalogue': categories,
    }
    return render_template('catalogue.html', **kwargs)


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
