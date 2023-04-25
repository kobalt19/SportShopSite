import requests


if __name__ == '__main__':
    print(requests.post('http://127.0.0.1:8080/api/goods', json={'name': 'Кроссовки 3', 'desc': 'Описание 2',
                                                                 'image': 'static/img/krossi.jpg', 'price': 3}).json())
