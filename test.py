import requests


if __name__ == '__main__':
    print(requests.post('http://127.0.0.1:8080/add_goods/', json={'name': 'Кроссовки_1', 'price': 500}).json())
