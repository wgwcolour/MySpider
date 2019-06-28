# coding=utf-8
import threading #多线程
import queue #队列
import time
import requests
import re #正则
# 第一页网址
baseUrl = 'https://gaokao.chsi.com.cn/sch/search--ss-on,searchType-1,option-qg,start-0.dhtml'
#网址翻页有规律，直接生成后面所有页码的网址,一共137页
urlQueue = queue.Queue()
for i in range(137):
    # 根据规律生成不同页码的链接参数
    pagenum = i*20
    # 将页码的链接参数放到链接里，生成完整链接
    url = "https://gaokao.chsi.com.cn/sch/search--ss-on,searchType-1,option-qg,start-{page}.dhtml".format(page=pagenum)
    # 将链接放到队列中，多线程要用
    urlQueue.put(url)



def fetchUrl(urlQueue):
    while True:
        try:
            # 不阻塞的读取队列数据
            url = urlQueue.get_nowait()
            # 队列大小
            print("剩余链接数：{}".format(urlQueue.qsize()))
        except Exception as e:
            break
        print("将采集：{}".format(url))
        try:
            # 请求网址获取响应内容
            response = requests.get(url)
            # 响应状态码
            responseCode = response.status_code
        except Exception as e:
            continue
        # 状态码200表示成功
        if responseCode == 200:
            #这部分就可以处理数据，解析、入库/存文件中
            # 获取响应内容的文本
            text = response.text
            #我使用正则解析,这个规则是取html代码中带有“学校名称”部分的td标签内的源码
            rule = re.compile("<td class=\"js-yxk-yxmc\">(.*?)</td>",re.S)
            # 用findall方法，取到所有的td标签源码
            tds = re.findall(rule,text)
            for td in tds:
                # 两种情况，有的td标签内直接就是学校名称，有的td标签内还包含了一个a标签
                if "<a" in td:
                    # 包含a标签,那就再用正则把a标签里的文本取出来
                    ruleA = re.compile("<a.*?>(.*?)</a>")
                    # 获取学校名字并且除去所有空格和\r
                    schoolName = re.findall(ruleA,td)[0].replace(' ','').replace('\r','')
                else:
                    # 不包含a标签，那直接取td里的文本，同样除去所有空格和\r
                    schoolName = td.replace(' ','').replace('\r','')
                # 有了学校名字，存到csv文件里
                with open("schoolName.csv",'a',encoding='utf-8') as f:
                    f.write(schoolName + '\n')





if __name__ == '__main__':
    startTime = time.time()
    threads = []
    # 可以调节线程数， 进而控制抓取速度
    threadNum = 1
    for i in range(0, threadNum):
        t = threading.Thread(target=fetchUrl, args=(urlQueue,))
        threads.append(t)
    for t in threads:
        t.start()
    for t in threads:
        # 多线程多join的情况下，依次执行各线程的join方法, 这样可以确保主线程最后退出， 且各个线程间没有阻塞
        t.join()
    endTime = time.time()
    print("采集耗时：",(endTime - startTime))
