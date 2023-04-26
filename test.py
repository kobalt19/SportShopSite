import requests


if __name__ == '__main__':
    for i in range(5, 8):
        print(requests.delete(f'http://127.0.0.1:8080/api/goods/{i}').json())
