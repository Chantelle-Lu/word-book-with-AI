import requests
import hashlib
import uuid
import time
import json

class YoudaoAPI:
    def __init__(self, app_key, app_secret, youdao_url='https://openapi.youdao.com/api'):
        self.app_key = app_key
        self.app_secret = app_secret
        self.youdao_url = youdao_url

    def encrypt(self, sign_str):
        """生成请求的签名。"""
        hash_algorithm = hashlib.sha256()
        hash_algorithm.update(sign_str.encode('utf-8'))
        return hash_algorithm.hexdigest()

    def truncate(self, q):
        """对查询字符串进行截断处理，用于签名。"""
        if q is None:
            return None
        size = len(q)
        return q if size <= 20 else q[0:10] + str(size) + q[size - 10:size]

    def connect(self, q, lang_type='auto', dicts='ec'):
        """构造请求并连接到有道词典API。"""
        curtime = str(int(time.time()))
        salt = str(uuid.uuid4())
        sign_str = self.app_key + self.truncate(q) + salt + curtime + self.app_secret
        sign = self.encrypt(sign_str)
        
        data = {
            'q': q,
            'langType': lang_type,
            'appKey': self.app_key,
            'salt': salt,
            'sign': sign,
            'signType': 'v3',
            'curtime': curtime,
            'dicts': {'count': 1, 'dicts': [[dicts]]},  # 以ec为例
            'docType': 'json'
        }

        headers = {'Content-Type': 'application/x-www-form-urlencoded'}
        response = requests.post(self.youdao_url, data=data, headers=headers)
        return response.json()



        


