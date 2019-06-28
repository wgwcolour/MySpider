# -*- coding: utf-8 -*-

# Define here the models for your spider middleware
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/spider-middleware.html

from scrapy import signals
import base64
import random

proxyServer = "http://http-dyn.abuyun.com:9020"
proxyUser = "HV3TF442816297JD"
proxyPass = "0EC646F1DAFD0B98"
proxyAuth = "Basic " + base64.urlsafe_b64encode(bytes((proxyUser + ":" + proxyPass), "ascii")).decode("utf8")


class JdwareDownloaderMiddleware(object):
    def process_response(self, request, response, spider):
        # 页面是否存在
        if response.status != 200:
            print('该次访问状态码错误【%d】' % response.status)
            return request
        return response

    def process_exception(self, request, exception, spider):
        print("**********")
        print("错误出现：【%s】" %(str(exception)))
        print("重试！")
        print("**********")
        return request



# 添加代理，靠引擎近，数值最小
class ProxyMiddleware(object):
    def process_request(self, request, spider):
        request.meta["proxy"] = proxyServer
        request.headers["Proxy-Authorization"] = proxyAuth
