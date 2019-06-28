# from sqlalchemy import text,create_engine
# # mymysql = ""
# # engine = create_engine(mymysql)
# import time
# import requests
# import json
# import queue,threading
# # 代理服务器
# proxyHost = "http-dyn.abuyun.com"
# proxyPort = "9020"
#
# # 代理隧道验证信息
# proxyUser = "H837U2D2589821ID"
# proxyPass = "C417682B9250824F"
#
# proxyMeta = "http://%(user)s:%(pass)s@%(host)s:%(port)s" % {
#   "host" : proxyHost,
#   "port" : proxyPort,
#   "user" : proxyUser,
#   "pass" : proxyPass,
# }
#
# proxies = {
#     "http"  : proxyMeta,
#     "https" : proxyMeta,
# }
#
# # resp = requests.get(targetUrl, proxies=proxies)
#
# headers = {
#     "User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36",
#     "Accept":"application/json",
#     "Accept-Encoding":"gzip, deflate, br",
#     "Accept-Language":"zh-CN,zh;q=0.9",
#     "Connection":"keep-alive",
#     "Content-Type":"application/x-www-form-urlencoded",
#     "Host":"m.tvmao.com",
#     "Origin":"https://m.tvmao.com",
#     "Referer":"https://m.tvmao.com/",
#     "X-Requested-With":"XMLHttpRequest"
#     }
# def exe(sql,type=1,pars = None):
#     print("执行开始")
#     pars = {} if pars is None else pars
#     connect = engine.connect()
#     T = None
#     if type == 1:
#         trans = connect.begin()
#         try:
#             connect.execute(text(sql),pars)
#             trans.commit()
#             print("执行成功")
#         except Exception as why:
#             print(why)
#             trans.rollback()
#             T = False
#         finally:
#             connect.close()
#         return T
#     else:
#         try:
#             t = connect.execute(text(sql),pars)
#             T = t.fetchall()
#             print("执行成功")
#         except Exception as why:
#             print(why)
#             pass
#         finally:
#             connect.close()
#         return T
#
# def getqueue():
#     q = queue.Queue()
#     sql = "select id,name from drama_copy where errorcode =2"
#     T = exe(sql, type=2)
#     if len(T) == 0:
#         return None
#     else:
#         for i in T:
#             q.put(i)
#         return q
#
# def func(q):
#     while True:
#         try:
#             T = q.get_nowait()
#             print("size:",q.qsize())
#         except:
#             print("队列结束")
#             break
#         rec = dict(T)
#         name = rec.get('name')
#         id = rec.get("id")
#         url = "https://m.tvmao.com/servlet/queryobject?type=all&term="
#         print(name)
#         # time.sleep(5)  # 这个必须等待。
#         u = url + name
#         try:
#             resp = requests.get(u, headers=headers, proxies=proxies)
#         except:
#             time.sleep(1)
#             resp = requests.get(u, headers=headers, proxies=proxies)
#         print(resp.status_code)
#         if resp.status_code == 200:
#             print(resp.text)
#             rp = json.loads(resp.text)
#             try:
#                 if len(rp) > 0:
#                     if isinstance(rp[0],int):
#                         print("请求错误")
#                         # time.sleep(10)
#                         continue
#                     name2 = rp[0].get("name")
#                     ui = "https://m.tvmao.com" + rp[0].get("url")
#                     if name == name2:
#                         # titleDict[ui] = name
#                         # with open('url.csv', 'a+', encoding='gbk') as m:
#                         #     m.write(name + ',' + ui + '\n')
#                         sql1 = "update drama_copy set url = :url,queryname=:name2 where id=:id"
#                         exe(sql1,pars=dict(id = id,name2 = name2,url = ui))
#                     else:
#                         # with open("nameerror.csv", 'a+', encoding='gbk') as s:
#                         #     s.write(name + ',' + name2 + "," + ui + '\n')
#                         sql1 = "update drama_copy set url = :url,queryname=:name2,errorcode=1 where id=:id"
#                         exe(sql1, pars=dict(id=id, name2=name2, url=ui))
#                 elif len(rp) == 0:
#                     sql1 = "update drama_copy set url = :url,queryname=:name2,errorcode=2 where id=:id"
#                     exe(sql1, pars=dict(id=id, name2='无搜索结果', url=''))
#             except Exception as e:
#                 print(e)
#                 # time.sleep(3)
#                 # with open("tryerror.csv", 'a+', encoding='gbk') as s:
#                 #     s.write(name + ',' + '' + "," + '' + '\n')
#         else:
#             print(resp.status_code)
#
# if __name__ == '__main__':
#     while True:
#         q = getqueue()
#         if q is None:
#             print("全部结束")
#             break
#         else:
#             startTime = time.time()
#             threads = []
#             # 可以调节线程数， 进而控制抓取速度
#             threadNum = 4
#             for i in range(0, threadNum):
#                 t = threading.Thread(target=func,args=(q,))
#                 threads.append(t)
#             for t in threads:
#                 t.start()
#             for t in threads:
#                 # 多线程多join的情况下，依次执行各线程的join方法, 这样可以确保主线程最后退出， 且各个线程间没有阻塞
#                 t.join()
#             endTime = time.time()
#             print("时间：",endTime-startTime)
#         print("等待五分钟")
#         time.sleep(10)
#         # func()
