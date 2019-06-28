# -*- coding: utf-8 -*-
import scrapy
import time
import json
import re
from jdWare.items import SpuItem
from jdWare.items import SkuItem
from jdWare.items import ReviewItem
from lxml import etree
import requests


class JdspiderSpider(scrapy.Spider):
    name = 'jdSpider'
    allowed_domains = ['mall.jd.com', 'item.jd.com','p.3.cn','club.jd.com','sclub.jd.com']
    headers = {
        "Referer": "https://bangolufsen.jd.com/view_search-396748-7559770-99-1-20-1.html",
        "User-Agent": "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.169 Safari/537.36"
    }
    headers_review = {
        "accept":"text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
        "accept-encoding":"gzip, deflate, br",
        "accept-language":"zh-CN,zh;q=0.9",
        "upgrade-insecure-requests":"1",
        "user-agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.92 Safari/537.36",
    }
    headers_detail = {
        "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
        "accept-encoding": "gzip, deflate, br",
        "accept-language": "zh-CN,zh;q=0.9",
        "cache-control": "max-age=0",
        "upgrade-insecure-requests": "1",
        "user-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.77 Safari/537.36",
    }

    def start_requests(self):
        ts = {
            "入耳式耳机": "https://module-jshop.jd.com/module/getModuleHtml.html?orderBy=99&direction=1&pageNo=1&categoryId=7559770&pageSize=20&pagePrototypeId=8&pageInstanceId=18825453&moduleInstanceId=161291089&prototypeId=55555&templateId=905542&appId=396748&layoutInstanceId=161291089&origin=0&shopId=1000000529&venderId=1000000529&callback=jshop_module_render_callback&_=1559801919467",
            "便携音箱": "https://module-jshop.jd.com/module/getModuleHtml.html?orderBy=99&direction=1&pageNo=1&categoryId=7559772&pageSize=20&pagePrototypeId=8&pageInstanceId=18825453&moduleInstanceId=161291089&prototypeId=55555&templateId=905542&appId=396748&layoutInstanceId=161291089&origin=0&shopId=1000000529&venderId=1000000529&callback=jshop_module_render_callback&_=1559801697059",
            "头戴式耳机": "https://module-jshop.jd.com/module/getModuleHtml.html?orderBy=99&direction=1&pageNo=1&categoryId=7559771&pageSize=20&pagePrototypeId=8&pageInstanceId=18825453&moduleInstanceId=161291089&prototypeId=55555&templateId=905542&appId=396748&layoutInstanceId=161291089&origin=0&shopId=1000000529&venderId=1000000529&callback=jshop_module_render_callback&_=1559801967028",
            "家具音箱": "https://module-jshop.jd.com/module/getModuleHtml.html?orderBy=99&direction=1&pageNo=1&categoryId=7559773&pageSize=20&pagePrototypeId=8&pageInstanceId=18825453&moduleInstanceId=161291089&prototypeId=55555&templateId=905542&appId=396748&layoutInstanceId=161291089&origin=0&shopId=1000000529&venderId=1000000529&callback=jshop_module_render_callback&_=1559802011971",
            "BeoSound系列": "https://module-jshop.jd.com/module/getModuleHtml.html?orderBy=99&direction=1&pageNo=1&categoryId=7006486&pageSize=20&pagePrototypeId=8&pageInstanceId=18825453&moduleInstanceId=161291089&prototypeId=55555&templateId=905542&appId=396748&layoutInstanceId=161291089&origin=0&shopId=1000000529&venderId=1000000529&callback=jshop_module_render_callback&_=1559802070838"
        }
        # url = "https://mall.jd.com/view_search-396748-7559770-99-1-24-1.html"
        for k, v in ts.items():
            meta = dict(Category_L1=k)
            yield scrapy.Request(v, meta=meta, headers=self.headers, dont_filter=True)

    # 解析一级分类
    def parse(self, response):
        meta = response.meta

        rule = re.compile("\"moduleText\":\"(.*?)\",\"moduleInstanceId", re.S)
        text = response.text.replace("\\r\\n", '').replace("\\", '')
        html = re.findall(rule, text)[0]
        tree = etree.HTML(html)
        li = tree.xpath("//li[@class='jSubObject gl-item']")
        for i in li:
            # 单个商品
            ul = i.xpath(".//ul/li")
            for idx,u in enumerate(ul):
                if idx>0: continue
                # 单个规格
                SPU_URL = u.xpath('./@data-href')[0]
                SPU_NUM = u.xpath('./@sid')[0]
                meta['SPU_URL'] = SPU_URL
                meta['SPU_NUM'] = SPU_NUM
                yield scrapy.Request(url='https:' + SPU_URL, headers=self.headers_detail, callback=self.parsedetail,
                                     meta=meta)

        # html = text.
        # print(1)

    def parsedetail(self, response):
        meta = response.meta
        meta['SPU_TIT'] = response.xpath("//div[@class='sku-name']/text()").extract()[0].replace('\n', '')
        meta['SPU_PIC'] = response.xpath("//ul[@class='lh']/li/img/@src").extract()
        meta['SPU_DES'] = response.xpath("//ul[@class='parameter2 p-parameter-list']/li/text()").extract()
        laburl = "https://cd.jd.com/promotion/v2?skuId={0}&area=3_51047_25704_0&shopId=1000000529&venderId=1000000529&cat=652%2C828%2C13662&isCanUseDQ=1&isCanUseJQ=1&platform=0&orgType=2&appid=1&_=1".format(meta['SPU_NUM'])
        meta['SPU_LAB'] = ''
        try:
            try:
                lab = requests.get(laburl,headers=self.headers)
            except:
                time.sleep(5)
                lab = requests.get(laburl, headers=self.headers)

            dat = json.loads(lab.text)
            if dat:
                ads = dat.get('ads')
                for i in ads:
                    meta['SPU_LAB'] = i.get('ad')
                    break
        except:
            pass
        meta['SPU_huabei'] = None #是否有分期
        huabeiURL = "https://btshow.jd.com/queryBtPlanInfo.do?callback=queryBtPlanInfo&sku={0}&cId=652%2C828%2C13662&num=1&amount=2448&sourceType=PC-XQ&shopId=1000000529&ver=1&areaId=3&isJd=false&_=1560328843992".format(meta['SPU_NUM'])
        try:
            try:
                hb = requests.get(huabeiURL, headers=self.headers)
            except:
                time.sleep(5)
                hb = requests.get(huabeiURL, headers=self.headers)
            hbt = hb.text
            rule = re.compile("({.*?)\)")
            js = re.findall(rule, hbt)
            if js:
                jso = json.loads(js[0])
                meta['SPU_huabei'] = jso.get('planInfos')
        except:
            pass

        s = response.xpath("//div[@class='Ptable-item']")
        a = {}
        for i in s:
            h3 = i.xpath("./h3/text()").extract()[0]
            dl = i.xpath(".//dl[@class='clearfix']")
            ds = {}
            for d in dl:
                dt = d.xpath("./dt/text()").extract()[0]
                dd = d.xpath("./dd/text()").extract()[0]
                ds[dt] = dd
            a[h3] = ds
        meta['SPU_SPEC'] = a
        meta['SPU_Product_PIC'] = response.xpath("//div[@id='J-detail-content']/img/@data-lazyload").extract()
        priceurl = "https://p.3.cn/prices/mgets?callback=jQuery6809710&type=1&area=3_51047_25704_0&pdtk=&pduid=15597881368431520999170&pdpin=&pin=null&pdbp=0&skuIds=J_{sku},J_7574276&ext=11100000&source=item-pc".format(
            sku=meta['SPU_NUM'])
        ndiv = response.xpath("//div[@id='choose-attr-1']")
        a = {}
        p = []
        v = []
        if ndiv:
            k = ndiv.xpath("./div[@class='dt ']/text()").extract()[0]
            dd =ndiv.xpath("./div[@class='dd']/div")

            for d in dd:
                sku = d.xpath("./@data-sku").extract()[0]
                value = d.xpath("./@data-value").extract()[0]
                nu = "https://p.3.cn/prices/mgets?callback=jQuery6809710&type=1&area=3_51047_25704_0&pdtk=&pduid=15597881368431520999170&pdpin=&pin=null&pdbp=0&skuIds=J_{sku},J_7574276&ext=11100000&source=item-pc".format(
            sku=sku)
                resp = requests.get(url=nu,headers=self.headers)
                text = self.getprice(resp)
                pr =text[0].get('p','')
                p.append(pr)
                v.append(value)
            a[k] = v
            a['价格'] = p
        item = SkuItem()
        item._values['SPU_NUM']=meta['SPU_NUM']
        item._values['SKU_TIT']=v
        item._values['SKU_PRICE']=p
        item._values['remark'] = a
        yield item


        yield scrapy.Request(url=priceurl, callback=self.priceparse, meta=meta, headers=self.headers)
    def getprice(self,response):
        rule = re.compile("\[.*?\]", re.S)
        text = json.loads(re.findall(rule, response.text)[0])
        return text
    def priceparse(self, response):
        meta = response.meta
        text = self.getprice(response)
        meta[
            'SPU_Price'] = text[0].get('p','')  # https://p.3.cn/prices/mgets?callback=jQuery6809710&type=1&area=3_51047_25704_0&pdtk=&pduid=15597881368431520999170&pdpin=&pin=null&pdbp=0&skuIds=J_7703395,J_7574276&ext=11100000&source=item-pc
        meta[
            'SPU_Price_Raw'] = text[0].get('op','')  # https://p.3.cn/prices/mgets?callback=jQuery6809710&type=1&area=3_51047_25704_0&pdtk=&pduid=15597881368431520999170&pdpin=&pin=null&pdbp=0&skuIds=J_7703395,J_7574276&ext=11100000&source=item-pc
        # meta['SPU_Sale_Month'] = None  # 月销量 京东没有
        url = "https://club.jd.com/comment/productCommentSummaries.action?referenceIds={sku}&callback=jQuery3825930&_=1559807830532".format(
            sku=meta['SPU_NUM'])
        yield scrapy.Request(url=url,headers=self.headers,callback=self.parsereview,meta=meta)
    def parsereview(self,response):
        meta = response.meta
        rule = re.compile("({.*?);",re.S)
        text = json.loads(re.findall(rule,response.text)[0][:-1])
        meta[
            'SPU_Review'] = text.get('CommentsCount')[0].get('CommentCountStr','')  # https://club.jd.com/comment/productCommentSummaries.action?referenceIds=5309719&callback=jQuery3825930&_=1559807830532
        meta['SPU_Score'] = text.get('CommentsCount')[0].get('GoodRateShow','')
        url = "https://sclub.jd.com/comment/productPageComments.action?callback=fetchJSON_comment98vv422&productId={sku}&score=0&sortType=5&page=0&pageSize=10&isShadowSku=0&fold=1".format(
            sku=meta['SPU_NUM'])
        yield scrapy.Request(url=url,headers=self.headers,meta=meta,callback=self.parsecontent)
        meta['reviewPageNum'] = 0
        yield scrapy.Request(url=url, headers=self.headers, meta=meta, callback=self.parseReview,
                             dont_filter=True)

    def parsecontent(self,response):
        rule = re.compile("({.*?)\);")
        meta = response.meta
        try:
            text = json.loads(re.findall(rule,response.text)[0])
            cont = text.get('hotCommentTagStatistics', '')
            a = {}
            for c in cont:
                a[c.get('name')] = c.get('count', 0)
            meta['SPU_Score_ALL'] = a
        except:
            print(response.text)
        item = SpuItem()
        item._values=meta
        yield item



    def parseReview(self, response):
        rule = re.compile("({.*?)\);",re.S)
        meta = response.meta
        noCommentsTarget = meta.get("noCommentsTarget",0)
        wNum = meta["SPU_NUM"]
        reviewPageNum = meta["reviewPageNum"]
        if "fetch" in response.text:
            try:
                text = re.findall(rule, response.text)[0]
            except:
                text = response.text
        else: text = response.text
        if response.text != '':
            data = json.loads(text)

            reviews = data["comments"]
            if reviews:
                for review in reviews:
                    reviewItem = ReviewItem()
                    reviewItem["SPU_NUM"] = wNum
                    reviewItem["SPU_TIT"] = review["referenceName"]
                    reviewItem["U_NAME"] = review["nickname"]
                    reviewItem["U_LEVEL"] = review["userLevelName"]
                    reviewItem["SKU_TIT"] = review["productColor"]
                    reviewItem["REV_TIME"] = review["creationTime"]
                    reviewItem["REV_CONTENT"] = review["content"]
                    reviewItem["REV_SCORE"] = review["score"]
                    reviewItem["REV_PIC"] = 1 if review.get("images") else 0
                    yield reviewItem
                print("REVIEW: 商品【%s】, 第【%s】页" % (str(wNum), str(reviewPageNum)))
                reviewPageNum += 1
                url = "https://sclub.jd.com/comment/productPageComments.action?productId=%s&score=0&sortType=6&page=%s&pageSize=10" % (wNum, str(reviewPageNum))
                yield scrapy.Request(url, headers = self.headers_review, callback = self.parseReview, meta = {"SPU_NUM":wNum, "reviewPageNum":reviewPageNum}, dont_filter = True)
            else:
                # 尝试2次，每次1分钟
                if noCommentsTarget < 2:
                    noCommentsTarget += 1
                    print("第%s次无comments!休眠60s后重试!" % str(noCommentsTarget))
                    time.sleep(60)
                    yield scrapy.Request(response.url, headers = self.headers_review, callback = self.parseReview, meta = {"SPU_NUM":wNum, "reviewPageNum":reviewPageNum, "noCommentsTarget":noCommentsTarget}, dont_filter = True)
                else:
                    print("========== 停止! ==========")
                    print("comments为空")
                    print(response.url)
        else:
            # 尝试2次，每次1分钟
            if noCommentsTarget < 2:
                noCommentsTarget += 1
                print("第%s次空字符串!休眠60s后重试!" % str(noCommentsTarget))
                time.sleep(60)
                yield scrapy.Request(response.url, headers=self.headers_review, callback=self.parseReview,
                                     meta={"SPU_NUM": wNum, "reviewPageNum": reviewPageNum,
                                           "noCommentsTarget": noCommentsTarget}, dont_filter=True)
            else:
                print("========== 停止! ==========")
                print("返回结果为空字符串")
                print(response.url)

    # ############## 每个关键词要修改的内容 ##############
    # keyword = "人工智能温控仪"
    # howmany = 10
    # ################################################
    # wareCounter = 0
    # name = 'jdSpider'
    # allowed_domains = ['so.m.jd.com']
    # pageNum = 1
    # pagesize = 100
    # headers_search = {
    #     "accept":"*/*",
    #     "accept-encoding":"gzip, deflate, br",
    #     "accept-language":"zh-CN,zh;q=0.9",
    #     "user-agent":"Mozilla/5.0 (iPhone; CPU iPhone OS 6_0 like Mac OS X) AppleWebKit/536.26 (KHTML, like Gecko) Version/6.0 Mobile/10A5376e Safari/8536.25",
    # }
    # headers_detail = {
    #     "accept":"text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
    #     "accept-encoding":"gzip, deflate, br",
    #     "accept-language":"zh-CN,zh;q=0.9",
    #     "cache-control":"max-age=0",
    #     "upgrade-insecure-requests":"1",
    #     "user-agent":"Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.77 Safari/537.36",
    # }
    # headers_rate = {
    #     "Accept":"text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
    #     "Accept-Encoding":"gzip, deflate, br",
    #     "Accept-Language":"zh-CN,zh;q=0.9",
    #     "Connection":"keep-alive",
    #     "Host":"club.jd.com",
    #     "Upgrade-Insecure-Requests":"1",
    #     "User-Agent":"Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.77 Safari/537.36",
    # }
    # headers_price = {
    #     "Accept":"text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
    #     "Accept-Encoding":"gzip, deflate, br",
    #     "Accept-Language":"zh-CN,zh;q=0.9",
    #     "Connection":"keep-alive",
    #     "Host":"pe.3.cn",
    #     "Upgrade-Insecure-Requests":"1",
    #     "User-Agent":"Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.77 Safari/537.36",
    # }
    # headers_review = {
    #     "accept":"text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
    #     "accept-encoding":"gzip, deflate, br",
    #     "accept-language":"zh-CN,zh;q=0.9",
    #     "upgrade-insecure-requests":"1",
    #     "user-agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.92 Safari/537.36",
    # }
    #
    #
    # def start_requests(self):
    #     # page从1开始，75页是最后一页，76页开始就没有了
    #     url = "https://so.m.jd.com/ware/search._m2wq_list?keyword=%s&datatype=1&page=%s&pagesize=%s" % (self.keyword, str(self.pageNum), str(self.pagesize))
    #     yield scrapy.Request(url, headers = self.headers_search, dont_filter = True)
    #
    #
    # def parse(self, response):
    #     pattern = re.compile(r"searchCB\((.*)\)")
    #     text = response.text
    #     text = text.replace('\n','')
    #     text = text.replace('\\','\\\\')
    #     # 特殊字符替换
    #     data = pattern.search(text).group(1)
    #     data = json.loads(data)
    #     # try:
    #     # 	data = json.loads(data)
    #     # except:
    #     # 	print("json解析错误")
    #     # 	with open("errorDATA.txt", "w", encoding = 'utf-8') as f:
    #     # 		f.write(data)
    #     # 	time.sleep(100)
    #     wares = data["data"]["searchm"]["Paragraph"]
    #     if wares:
    #         for ware in wares:
    #             self.wareCounter += 1
    #             wNum = "P%s.%s" % (str(self.howmany), str(self.wareCounter))
    #             wId = ware["wareid"]
    #             url = "https://item.jd.com/%s.html" % str(wId)
    #             yield scrapy.Request(url, headers = self.headers_detail, callback = self.parseWareDetail, meta = {'wNum':wNum, 'wId':wId}, dont_filter = True)
    #         print("【%s】第【%s】页, 共【%s】件商品" % (self.keyword, str(self.pageNum), str(len(wares))))
    #         # 下一页
    #         self.pageNum += 1
    #         url = "https://so.m.jd.com/ware/search._m2wq_list?keyword=%s&datatype=1&page=%s&pagesize=%s" % (self.keyword, str(self.pageNum), str(self.pagesize))
    #         yield scrapy.Request(url, headers = self.headers_search, dont_filter = True)
    #     else:
    #         print("【%s】最后一页+1" % self.keyword)
    #
    #
    # def parseWareDetail(self, response):
    #     meta = response.meta
    #     # SPU_NUM
    #     wNum = meta["wNum"]
    #     # SPU_ID
    #     wID = meta["wId"]
    #     # SPU_URL: 商品链接
    #     wUrl = response.url
    #     # SPU_TIT: 商品名称
    #     # wName = response.xpath(".//div[@class='sku-name']/text()").extract()[0].strip()
    #     wName_temp = response.xpath(".//div[@class='sku-name']")[0]
    #     wName = wName_temp.xpath("string(.)").extract()[0].strip()
    #     # SPU_DESP: 商品介绍
    #     wDesp = []
    #     allDesp = response.xpath(".//div[@class='p-parameter']/ul/li")
    #     for i in allDesp:
    #         desp = i.xpath("string(.)").extract()[0].strip()
    #         wDesp.append(desp)
    #     # SPU_SPEC: 商品规格
    #     wSpec = []
    #     allSpec = response.xpath(".//div[@class='Ptable']/div/dl/dl")
    #     for i in allSpec:
    #         i1 = i.xpath("./dt/text()").extract()[0].strip()
    #         i2 = i.xpath("./dd/text()").extract()[0].strip()
    #         i3 = ":".join([i1,i2])
    #         wSpec.append(i3)
    #     url = "https://club.jd.com/comment/productCommentSummaries.action?referenceIds=%s" % str(wID)
    #     yield scrapy.Request(url, headers = self.headers_rate, callback = self.parseRate, meta = {"wNum":wNum, "wID":wID, "wName":wName, "wDesp":wDesp, "wSpec":wSpec, "wUrl":wUrl}, dont_filter = True)
    #     # SKU项目，不同版本
    #     all_SPU_NUM = response.xpath(".//div[@id='choose-attrs']/div[1]/div[@class='dd']/div/@data-sku").extract()
    #     all_SKU_TIT = response.xpath(".//div[@id='choose-attrs']/div[1]/div[@class='dd']/div/@data-value").extract()
    #     if all_SPU_NUM:
    #         temp = ','.join(all_SPU_NUM)
    #         url = "https://pe.3.cn/prices/mgets?skuids=%s" % temp
    #         yield scrapy.Request(url, headers = self.headers_price, callback = self.parsePrice, meta = {"wNum":wNum, "wID":wID, "all_SPU_NUM":all_SPU_NUM, "all_SKU_TIT":all_SKU_TIT}, dont_filter = True)
    #     else:
    #         all_SPU_NUM = [wID,]
    #         all_SKU_TIT = [wName,]
    #         url = "https://pe.3.cn/prices/mgets?skuids=%s" % wID
    #         yield scrapy.Request(url, headers = self.headers_price, callback = self.parsePrice, meta = {"wNum":wNum, "wID":wID, "all_SPU_NUM":all_SPU_NUM, "all_SKU_TIT":all_SKU_TIT}, dont_filter = True)
    #     # Review项目，评论，page从0开始
    #     reviewPageNum = 0
    #     url = "https://sclub.jd.com/comment/productPageComments.action?productId=%s&score=0&sortType=6&page=%s&pageSize=10" % (wID, str(reviewPageNum))
    #     yield scrapy.Request(url, headers = self.headers_review, callback = self.parseReview, meta = {"wNum":wNum, "wID":wID, "reviewPageNum":reviewPageNum}, dont_filter = True)
    #
    #
    # # SPU项目全部爬取完毕
    # def parseRate(self, response):
    #     meta = response.meta
    #     wNum = meta["wNum"]
    #     wID = meta["wID"]
    #     wUrl = meta["wUrl"]
    #     wName = meta["wName"]
    #     wDesp = meta["wDesp"]
    #     wSpec = meta["wSpec"]
    #     text = response.text
    #     data = json.loads(text)
    #     # SPU_RATE: 商品口碑得分
    #     wGoodRate = data["CommentsCount"][0]["GoodRate"]
    #     # SPU_REVNUM: 总评论数量
    #     wRevNum = data["CommentsCount"][0]["CommentCount"]
    #     # SPU_TREVNUM: 实际评论数量
    #     wTrevNum = data["CommentsCount"][0]["CommentCount"] - data["CommentsCount"][0]["DefaultGoodCount"]
    #     spuItem = SpuItem()
    #     spuItem["SPU_NUM"] = wNum
    #     # spuItem["SPU_ID"] = wID
    #     spuItem["SPU_URL"] = wUrl
    #     spuItem["SPU_TIT"] = wName
    #     spuItem["SPU_DESP"] = wDesp
    #     spuItem["SPU_SPEC"] = wSpec
    #     spuItem["SPU_RATE"] = wGoodRate
    #     spuItem["SPU_REVNUM"] = wRevNum
    #     spuItem["SPU_TREVNUM"] = wTrevNum
    #     print("SPU: 商品【%s】" % str(wID))
    #     yield spuItem
    #
    #
    # # SKU项目全部爬取完毕
    # def parsePrice(self, response):
    #     meta = response.meta
    #     wNum = meta["wNum"]
    #     wID  = meta["wID"]
    #     all_SPU_NUM = meta["all_SPU_NUM"]
    #     all_SKU_TIT = meta["all_SKU_TIT"]
    #     data = json.loads(response.text)
    #     for i in zip(all_SPU_NUM, all_SKU_TIT, data):
    #         skuItem = SkuItem()
    #         skuItem["SPU_NUM"] = wNum
    #         skuItem["SKU_ID"]  = i[0]
    #         skuItem["SKU_TIT"] = i[1]
    #         skuItem["SKU_PRICEBF"] = float(i[2]["op"])
    #         skuItem["SKU_PRICEAF"] = float(i[2]["p"])
    #         print("SKU: 商品【%s】" % str(wID))
    #         yield skuItem
    #
    #
    # # REVIEW项目
    # def parseReview(self, response):
    #     meta = response.meta
    #     noCommentsTarget = meta.get("noCommentsTarget",0)
    #     wNum = meta["wNum"]
    #     wID  = meta["wID"]
    #     reviewPageNum = meta["reviewPageNum"]
    #     text = response.text
    #     data = json.loads(text)
    #     reviews = data["comments"]
    #     if reviews:
    #         for review in reviews:
    #             reviewItem = ReviewItem()
    #             reviewItem["SPU_NUM"] = wNum
    #             reviewItem["SPU_TIT"] = review["referenceName"]
    #             reviewItem["U_NAME"] = review["nickname"]
    #             reviewItem["U_LEVEL"] = review["userLevelName"]
    #             reviewItem["SKU_TIT"] = review["productColor"]
    #             reviewItem["REV_TIME"] = review["creationTime"]
    #             reviewItem["REV_CONTENT"] = review["content"]
    #             reviewItem["REV_SCORE"] = review["score"]
    #             reviewItem["REV_PIC"] = 1 if review.get("images") else 0
    #             yield reviewItem
    #         print("REVIEW: 商品【%s】, 第【%s】页" % (str(wID), str(reviewPageNum)))
    #         reviewPageNum += 1
    #         url = "https://sclub.jd.com/comment/productPageComments.action?productId=%s&score=0&sortType=6&page=%s&pageSize=10" % (wID, str(reviewPageNum))
    #         yield scrapy.Request(url, headers = self.headers_review, callback = self.parseReview, meta = {"wNum":wNum, "wID":wID, "reviewPageNum":reviewPageNum}, dont_filter = True)
    #     else:
    #         # 尝试2次，每次1分钟
    #         if noCommentsTarget < 2:
    #             noCommentsTarget += 1
    #             print("第%s次无comments!休眠60s后重试!" % str(noCommentsTarget))
    #             time.sleep(63)
    #             yield scrapy.Request(response.url, headers = self.headers_review, callback = self.parseReview, meta = {"wNum":wNum, "wID":wID, "reviewPageNum":reviewPageNum, "noCommentsTarget":noCommentsTarget}, dont_filter = True)
    #         else:
    #             print("========== 停止! ==========")
    #             print("comments为空")
    #             print(response.url)
