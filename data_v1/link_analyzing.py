#encoding:utf-8

import pickle
import requests
import to_json
from urllib import parse


content = open('result_array.pkl','rb')
data = pickle.load(content)


def short_link(origin):
    origin = parse.quote(origin).replace('%3A',':')
    print(origin)

    host = 'https://dwz.cn'
    path = '/admin/v2/query'
    url = host + path
    method = 'POST'
    content_type = 'application/json'

    token = '658a58042d4e099d9feee9cf23d19b16'

    bodys = {'shortUrl': origin}

    # 配置headers
    headers = {'Content-Type': content_type, 'Token': token}

    # 发起请求
    response = requests.post(url=url, data=to_json.dumps(bodys), headers=headers)

    # 读取响应
    print(response.text)


def analyze_link(i):
    str = 'https://ctd-1257758577.cos.ap-guangzhou.myqcloud.com/' + i['addr']
    str = str.replace('\\','/')
    return str




