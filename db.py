import requests


def get_users():
    response = requests.get('http://54.74.230.254/user/all')
    return response.json()


