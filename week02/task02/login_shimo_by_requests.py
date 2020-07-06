import requests
from fake_useragent import UserAgent


class ShiMo:
    def __init__(self, data):
        self.data = data
        self.login_link = 'https://shimo.im/lizard-api/auth/password/login'
        self.profile_link = 'https://shimo.im/lizard-api/users/me'
        self.ua = UserAgent().random
        self.login_headers = {
            'authority': 'shimo.im',
            'pragma': 'no-cache',
            'cache-control': 'no-cache',
            'origin': 'https://shimo.im',
            'x-requested-with': 'XmlHttpRequest',
            'x-source': 'lizard-desktop',
            'user-agent': self.ua,
            'dnt': '1',
            'content-type': 'application/x-www-form-urlencoded; charset=utf-8',
            'accept': '*/*',
            'sec-fetch-site': 'same-origin',
            'sec-fetch-mode': 'cors',
            'referer': 'https://shimo.im/login?from=home',
            'accept-encoding': 'gzip, deflate, br',
            'accept-language': 'zh-CN,zh;q=0.9,en;q=0.8',
        }
        self.get_headers = {
            'authority': 'shimo.im',
            'pragma': 'no-cache',
            'cache-control': 'no-cache',
            'accept': 'application/vnd.shimo.v2+json',
            'dnt': '1',
            'x-requested-with': 'XmlHttpRequest',
            'user-agent': self.ua,
            'sec-fetch-site': 'same-origin',
            'sec-fetch-mode': 'cors',
            'referer': 'https://shimo.im/dashboard',
            'accept-encoding': 'gzip, deflate, br',
            'accept-language': 'zh-CN,zh;q=0.9,en;q=0.8',
    }
        self.session = requests.Session()

    def login(self):
        try:
            resp = self.session.post(
                url=self.login_link,
                data=self.data,
                headers=self.login_headers)
            print(f'login status: {resp.status_code}')
        except Exception as e:
            print(f'login error: {e}')
    
    def get_profile(self):
        try:
            resp = self.session.get(
                url=self.profile_link,
                headers=self.get_headers,
                cookies=self.session.cookies)
            data = resp.json()
            print(f'profile info:')
            print(f'''
                id: {data["id"]}
                name: {data["name"]}
                email: {data["email"]}
                createdAt: {data["createdAt"]}''')
        except Exception as e:
            print(f'get profile error: {e}')


if __name__ == '__main__':
    email = input('请输入用户名：')
    psw = input('请输入密码：')
    data = {
        'email': email,
        'mobile': '+86undefined',
        'password': psw
    }

    shimo_user = ShiMo(data)
    shimo_user.login()
    shimo_user.get_profile()

