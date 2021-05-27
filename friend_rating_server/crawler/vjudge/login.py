import requests


def login(session: requests.Session, username: str, password: str) -> bool:
    session.get('https://vjudge.net')
    rsp = session.post('https://vjudge.net/user/login', data={
        "username": username,
        "password": password,
    })
    return rsp.status_code == 200 and rsp.text == 'success'
