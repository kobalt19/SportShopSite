import flask

app = flask.Flask(__name__)
app.config['SECRET_KEY'] = 'yandexlyceum_secret_key'


def main():
    app.run(host='127.0.0.1', port=8080)


if __name__ == '__main__':
    main()
