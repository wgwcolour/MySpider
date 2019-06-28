import requests
import json
from pymongo import MongoClient
from sqlalchemy import create_engine, text
import threading,queue
import uuid
# MongoDB设置
MONGO_HOST = "127.0.0.1"  # 主机IP
MONGO_PORT = 27017  # 端口号
MONGO_DB = "heb"  # 库名

# mongodb保存数据
def mongo_save_data(tb,data):
    conn = MongoClient(MONGO_HOST, MONGO_PORT)
    db = conn[MONGO_DB]
    my_set = db[tb]
    data=data
    my_set.insert_one(data)

    conn.close()
headers = {
    'Accept': "*/*",
    'Accept-Encoding': "gzip, deflate",
    'Accept-Language': "zh-CN,zh;q=0.9",
    'Content-Type': "application/json",
    'Host': "www.hebzhiyuan.com",
    'Origin': "http://www.hebzhiyuan.com",
    'Referer': "http://www.hebzhiyuan.com/",
    'User-Agent': "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.169 Safari/537.36",
    'Cache-Control': "no-cache",
    }

headers2 = {
    'Accept': "*/*",
    'Accept-Encoding': "gzip, deflate",
    'Accept-Language': "zh-CN,zh;q=0.9",
    'Host': "www.hebzhiyuan.com",
    'Origin': "http://www.hebzhiyuan.com",
    'Referer': "http://www.hebzhiyuan.com/",
    'User-Agent': "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.169 Safari/537.36",
    'Connection':'keep-alive',
    'Content-Length':'0'
    }

def getTOKEN(response):
    return response.headers.get('x-token')
if __name__ == '__main__':
    import time
    # 先登录获取x-token
    loginURL= "http://www.hebzhiyuan.com/api/user/login"
    pwd = {"uid":"19004130234","pwd":"13354451"}
    login = requests.post(loginURL,data=json.dumps(pwd),headers=headers)
    token = getTOKEN(login)
    url = "http://www.hebzhiyuan.com/api/colleges/enrollments"
    # payload = "{\"parameters\":{},\"_pager\":{\"size\":15,\"page\":1}}"
    dic = {}
    for i in range(1,313):# 313
        print(i)
        payload = {"parameters":{},"_pager":{"size":15,"page":i}}
        headers['Authorization'] = token
        # headers2['Authorization'] = token
        response = requests.post(url,data=json.dumps(payload),headers=headers)
        token=getTOKEN(response) if getTOKEN(response) else token

        # newurl = 'http://www.hebzhiyuan.com/api/colleges/info/{0}'.format(10006)
        # resp = requests.post(url, headers=headers2)
        # print(1)
        result = json.loads(response.text)
        items = result[1].get('items')
        for i in items:
            school = i[0]

            data = i[1]
            if school in dic:
                dic[school]['list'].append(data)
            else:
                dic[school] = {}
                dic[school]['list'] = [data]
                yxdm = data.get('yxdm','')
                dic[school]['yxdm'] = yxdm
                headers2['Authorization'] = token
                # 请求院校内页
                time.sleep(2)
                newurl = 'http://www.hebzhiyuan.com/api/colleges/info/{0}'.format(yxdm)
                resp = requests.post(newurl,headers=headers2)
                dic[school]['detail'] = json.loads(resp.text)
        time.sleep(3)

    for k,v in dic.items():
        dics = {}
        dics['name'] = k
        dics['data'] = v
        mongo_save_data('wen',dics)