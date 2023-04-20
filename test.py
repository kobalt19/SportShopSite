import requests


if __name__ == '__main__':
    print(requests.get('http://127.0.0.1:8080/remove_from_order/1').content)
