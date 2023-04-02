from flask import Flask, render_template

app = Flask(__name__)
app.config['SECRET_KEY'] = 'yandexlyceum_secret_key'


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
