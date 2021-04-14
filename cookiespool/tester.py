import json
import requests
from requests.exceptions import ConnectionError
from cookiespool.db import *


class ValidTester(object):
    def __init__(self, website='default'):
        self.website = website
        self.cookies_db = RedisClient('cookies', self.website)
        self.accounts_db = RedisClient('accounts', self.website)
    
    def test(self, username, cookies):
        raise NotImplementedError
    
    def run(self):
        cookies_groups = self.cookies_db.all()
        for username, cookies in cookies_groups.items():
            self.test(username, cookies)


# 新浪微博的检测器
class WeiboValidTester(ValidTester):
    def __init__(self, website='weibo'):
        ValidTester.__init__(self, website)
    
    def test(self, username, cookies):
        print('正在测试Cookies', '用户名:', username)
        try:
            cookies = json.loads(cookies)
        except TypeError:
            print('Cookies不合法', username)
            self.cookies_db.delete(username)
            print('删除Cookies', username)
            return
        try:
            test_url = TEST_URL_MAP[self.website]
            response = requests.get(test_url, cookies=cookies, timeout=5, allow_redirects=False)
            if response.status_code == 200:
                print('Cookies有效', username)
            else:
                print(response.status_code, response.headers)
                print('Cookies失效', username)
                self.cookies_db.delete(username)
                print('删除Cookies', username)
        except ConnectionError as e:
            print('发生异常', e.args)


# 拉勾的检测器
class LagouValidTester(ValidTester):
    def __init__(self, website='lagou'):
        ValidTester.__init__(self, website)

    def test(self, username, cookies):
        print('正在测试拉勾Cookies', '用户名:', username)
        try:
            cookies = json.loads(cookies)
        except TypeError:
            print("Cookies不合法", username)
            self.cookies_db.delete(username)
            print("删除Cookies", username)
            return
        try:
            test_url = TEST_URL_MAP[self.website]
            response = requests.get(test_url, cookies=cookies, timeout=5, allow_redirects=False)
            if response.status_code == 200:
                print("拉勾网状态码{0}，Cookies有效帐号为：{1}".format(response.status_code, username))
            else:
                print(response.status_code, response.headers)
                print("Cookies失效", username)
                self.cookies_db.delete(username)
                print("删除Cookies", username)

        except ConnectionError as e:
            print("发生异常", e.args)


# 哔哩检测器
class BilibiliValidTester(ValidTester):
    def __init__(self, website='bilibili'):
        ValidTester.__init__(self, website)

    def test(self, username, cookies):
        print('正在测试哔哩哔哩Cookies', '用户名:', username)
        try:
            cookies = json.loads(cookies)
        except TypeError:
            print("Cookies不合法", username)
            self.cookies_db.delete(username)
            print("删除Cookies", username)
            return
        try:
            test_url = TEST_URL_MAP[self.website]
            response = requests.get(test_url, cookies=cookies, timeout=5, allow_redirects=False)
            if response.status_code == 200:
                print("哔哩哔哩网状态码{0}，Cookies有效帐号为：{1}".format(response.status_code, username))
            else:
                print(response.status_code, response.headers)
                print("Cookies失效", username)
                self.cookies_db.delete(username)
                print("删除Cookies", username)

        except ConnectionError as e:
            print("发生异常", e.args)


if __name__ == '__main__':
    WeiboValidTester().run()