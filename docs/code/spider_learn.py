import requests

def get_data():
    response = requests.get('http://127.0.0.1:5000/news/getnews/')
    print(response.content.decode())


if __name__ == '__main__':
    get_data()