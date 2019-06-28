# -*- coding: utf-8 -*-
import scrapy
import json
import re
from urllib import parse
import time
from xiaohongshu.items import XiaohongshuItem,Review,SKU

class XhsspiderSpider(scrapy.Spider):
    name = 'xhsSpider'
    allowed_domains = ['www.xiaohongshu.com']
    # 几个重要的参数 TODO 登陆过期需要更新这里
    review = False # 是否采集评论，是评论不是笔记
    search_id = "5CDA4F6DF7A4AABB37670F25157F8561"
    sign = "aa5d3fc98564911509fad53456646aec"
    sid = "session.1560752124908783911929"
    page_count= 1000 # 每种商品取1000个
    ######################################
    headers = {
        "Host":"www.xiaohongshu.com",
        "Accept":"application/json, text/plain, */*",
        "Cookie":"xhs_spid.5dde=b4c93751b6f3593e.1560752144.1.1560752147.1560752144.ea369523-707e-4f7a-aa8d-3259a92891c0; xhs_spses.5dde=*; beaker.session.id=829e2dc1a3b25c4529e5aad1ba24134a1eca2c43gAJ9cQEoVQh1c2VyaWQuMXECY2Jzb24ub2JqZWN0aWQKT2JqZWN0SWQKcQMpgXEEVQxc9MsFAAAAABIAMtlxBWJVA19pZHEGVSA4MTNhYWQ2M2Y2Yzg0M2JlYjk1OGRkZTA4NjRhNDIyOHEHVQ5fYWNjZXNzZWRfdGltZXEIR0HXQcwCGzCYVQ5fY3JlYXRpb25fdGltZXEJR0HXQcwCGzCQVQtzZXNzaW9uaWQuMXEKVR5zZXNzaW9uLjE1NjA3NTIxMjQ5MDg3ODM5MTE5MjlxC3Uu; beaker.session.id=829e2dc1a3b25c4529e5aad1ba24134a1eca2c43gAJ9cQEoVQh1c2VyaWQuMXECY2Jzb24ub2JqZWN0aWQKT2JqZWN0SWQKcQMpgXEEVQxc9MsFAAAAABIAMtlxBWJVA19pZHEGVSA4MTNhYWQ2M2Y2Yzg0M2JlYjk1OGRkZTA4NjRhNDIyOHEHVQ5fYWNjZXNzZWRfdGltZXEIR0HXQcwCGzCYVQ5fY3JlYXRpb25fdGltZXEJR0HXQcwCGzCQVQtzZXNzaW9uaWQuMXEKVR5zZXNzaW9uLjE1NjA3NTIxMjQ5MDg3ODM5MTE5MjlxC3Uu",
        "User-Agent":"discover/6.0.1 (iPhone; iOS 10.3.3; Scale/2.00) Resolution/750*1334 Version/6.0.1 Build/6001009 Device/(Apple Inc.;iPhone7,2) NetType/WiFi",
        "Accept-Encoding":"gzip, deflate",
    }

    def start_requests(self):
        # 列表
        url = "https://www.xiaohongshu.com/api/store/v1/classifications?sid={0}".format(self.sid)
        yield scrapy.Request(url=url,headers=self.headers)

    # 从url中解析出参数键值对
    def getpars(self,url):
        result = parse.parse_qs(parse.urlparse(url).query)
        return result


    # 1、解析分类列表
    def parse(self, response):
        meta = dict()
        content = response.text
        jsonText = json.loads(content)
        data = jsonText.get('data')
        # count = 0
        for entrie in data:
            Category_L1 = entrie.get('name')# 一级分类
            meta['Category_L1'] = Category_L1
            try:
                for products in entrie.get('entries'):# 虚假的二级分类
                    level2 = products.get('entries') if products.get('entries') else [products] # 兼容【配饰】，它没有虚假的二级分类
                    for product in level2:# 真实的二级分类
                        # print(count)
                        # if count > 0:
                        #     break
                        Category_L2 = product.get('name')# 二级分类
                        meta['Category_L2'] = Category_L2
                        meta['page'] = 1
                        link2 = product.get('link')
                        if link2:
                            pars = self.getpars(link2)
                            t = time.time()
                            url = "https://www.xiaohongshu.com/api/store/ps/products/v3?api_extra=" + \
                                pars.get('source')[0] + "&deviceId=B47DE2A5-04B2-4BBA-9BD2-FF2B3AAF5CBC&device_fingerprint=20190429235719aaae025d555fbfaf8641b3905bcc69400180654b164c508c&device_fingerprint1=20190429235719aaae025d555fbfaf8641b3905bcc69400180654b164c508c&fid=1559546601-0-0-f0491099-ddb3-460b-8351-df19018c92eb&keyword=" + \
                                pars.get('keyword')[0] +"&page=1&page_pos=0&platform=iOS&search_id=" + \
                                self.search_id + '&sid=' + self.sid + "&sign=" + self.sign + \
                                  "&sort=sales_qty&size=20&source=classification&t=" + \
                                str(int(t))

                            # count += 1
                            yield scrapy.Request(url=url,callback=self.paserpage,meta=meta)
            except:
                print(1)
    # 解析分页
    def paserpage(self,response):
        meta = response.meta
        # 获取页码
        page=meta['page']
        # 获取json
        content = json.loads(response.text)
        data = content['data']
        items = data.get('items')
        if items:
            for idx,i in enumerate(items):
                meta['SPU_NUM'] = i.get('id')
                meta['Sale_Rank'] = (idx+1)+(page-1)*20
                meta['Liking'] = i.get('fav_info',{}).get('fav_count')
                meta['SPU_URL'] = i.get('link').replace('https://pages.xiaohongshu.com',"www.xiaohongshu.com")

                #
                #
                # prices = i.get('item_price')
                # for p in prices:
                #     if p.get('type') =="sale_price":
                #         meta['SPU_Price'] =p.get('price')
                #     elif p.get('type') == 'origin_price':
                #         meta['SPU_Price_Raw'] = p.get('price')

                homeurl = "https://www.xiaohongshu.com/api/store/jpd/{0}/static?anti_crawler=1&sid={1}".format(meta['SPU_NUM'],self.sid)
                yield scrapy.Request(url=homeurl,callback=self.parseHome,headers=self.headers,meta=meta)
        # if page<1:# 小于50页就继续翻页
        if page<self.page_count//20:# 小于50页就继续翻页
            rule = re.compile("&page=[0-9]+&")
            nexturl = re.sub(rule,"&page={0}&".format(page+1),response.url)
            meta['page']=page+1
            yield scrapy.Request(url=nexturl, callback=self.paserpage, headers=self.headers, meta=meta)
    # 解析主页
    def parseHome(self,response):
        meta = response.meta
        keyword = None
        data = json.loads(response.text).get('data')
        items = data.get('items')
        shops = []
        # 存店铺id，数量组合，价格id。最后把当前店铺id的取出来就是不同规格的商品了
        tdic = {}
        #{"id":[{"num":"","pid":""}]}
        for item in items:
            shop = {}
            spid = item.get('seller').get('id')## 店铺id，后面需要用到
            pid = item.get('id')# 价格id
            variants = item.get('variants')
            d = {"pid":pid}
            for i in variants:
                d[i.get('name')]=i.get('value')
                shop[i.get('name')]=i.get('value')
        # item = items[0] if items else dict()
            if spid in tdic:
                tdic[spid].append(d)
            else:
                tdic[spid] = [d]
            if item.get('id') == meta['SPU_NUM']:
                keyword = item.get('share_info').get('tit')
                meta['sellerId'] = spid
                meta['SPU_TIT'] = item.get('name')
                meta['SPU_Brand'] = item.get('brand').get('name')
                meta['SPU_Brand_GEO'] = item.get('brand').get('country')
                meta['SPU_Coupon'] = item.get('coupon_text_overview')# TODO 薯券
                meta['SPU_Product_PIC'] = []
                plist = item.get('detail',{}).get('image_desc',{}).get('images',[])
                for i in plist:
                    meta['SPU_Product_PIC'].append("https:" + i.get('link'))
                plist = item.get('images')
                meta['SPU_PIC'] = []
                for i in plist:
                    meta['SPU_PIC'].append("https:" + i.get('link'))
                meta['SPU_DES'] = item.get('desc')

                attr = []
                for i in item.get('detail').get('attributes'):
                    a = {}
                    a['name'] = i.get('attribute_name')
                    a['value'] = i.get('text')
                    attr.append(a)
                for i in item.get('variants'):
                    a = {}
                    a['name'] = i.get('name')
                    a['value'] = i.get('value')
                    attr.append(a)
                attr.append(dict(name='商品名称',value=item.get('short_name')))
                meta['SPU_SPEC'] = attr
                meta['SPU_BUS'] = item.get('seller').get('name')
                # meta['SPU_BUS_Other'] = '' #TODO 其他家相同商品是什么？？推荐页？
            # 这里边找到全部卖相同商品的店铺
            shop['name'] = item.get('seller').get('name')
            shop['id'] = item.get('id')
            shops.append(shop)

        meta['skus'] = tdic[meta['sellerId']]
        meta['SPU_BUS_Other'] = shops
        url = "https://www.xiaohongshu.com/api/store/jpd/{0}?xhs_g_s=&anti_crawler=1&{1}".format(meta['SPU_NUM'],self.sid)
        # 价格和折扣信息
        yield scrapy.Request(url=url,callback=self.parsePrice,meta=meta,headers=self.headers)
        # 评论信息
        if self.review:
            reviewURL = "https://www.xiaohongshu.com/api/store/review/{0}/product_review?page=0&perPage=10&tab=2&fold=0&sid={1}".format(meta['SPU_NUM'],self.sid)
            meta['tpage'] = 0
            yield scrapy.Request(url=reviewURL,callback=self.parsereview,meta=meta,headers=self.headers)
        # 笔记
        # if keyword:
        #     notesURL = "https://www.xiaohongshu.com/api/sns/v9/search/notes?allow_rewrite=1&api_extra=&deviceId=B47DE2A5-04B2-4BBA-9BD2-FF2B3AAF5CBC&device_fingerprint=20190429235719aaae025d555fbfaf8641b3905bcc69400180654b164c508c&device_fingerprint1=20190429235719aaae025d555fbfaf8641b3905bcc69400180654b164c508c&fid=1559546601-0-0-f0491099-ddb3-460b-8351-df19018c92eb&keyword={keyword}&keyword_type=normal&lang=zh&page=1&page_pos=0&page_size=20&platform=iOS&search_id={search_id}&sid={sid}&sign={sign}&sort=general&source=goods_detail&t={t}".format(keyword=keyword,search_id=self.search_id,sid=self.sid,sign=self.sign,t=int(time.time()))

    # 解析评论
    def parsereview(self,response):
        meta = {}
        SPU_NUM = response.meta['SPU_NUM']
        page=response.meta.get('tpage')# 当前页码
        zpage = response.meta.get('zpage')

        meta['SPU_NUM'] = SPU_NUM
        text = response.text
        tjs = json.loads(text)
        data = tjs.get('data',{})
        if data:
            if page == 0:
                total = data.get('total',0)
                foldCommentTotal = data.get('foldCommentTotal',0)
                total += foldCommentTotal
                zpage = total//10# 总页码
                meta['zpage'] = zpage  # 总页码
            reviews = data.get('reviews')
            for i in reviews:
                meta['U_NAME'] = i.get('userInfo',{}).get('userName')
                meta['U_LEVEL'] = "R" if i.get('userInfo',{}).get('member') else ''
                meta['Favorites'] = i.get('itemScore')#TODO
                meta['Thumb_up'] = i.get('favCount')
                meta['REV_CONTENT'] = i.get('text')
                meta['REV_PIC'] = i.get('images')
                descendants = i.get('descendants')
                meta['REV_CONTENT2'] = []
                for d in descendants:
                    a = {}
                    a['text'] = d.get('text')
                    a['images'] = d.get('images')
                    meta['REV_CONTENT2'].append(a)

                meta['SKU_TIT'] = ''# 购买的产品类型 非结构化，需要从笔记中挖取
                item = Review()
                item._values=meta
                yield item
            # 翻页
            npage = page+1
            if npage <meta['zpage']:
            # if npage <1:
                reviewURL = "https://www.xiaohongshu.com/api/store/review/{0}/product_review?page={1}&perPage=10&tab=2&fold=0&sid={2}".format(
                    meta['SPU_NUM'],npage, self.sid)
                meta['tpage'] = npage
                yield scrapy.Request(url=reviewURL, callback=self.parsereview, meta=meta, headers=self.headers)



        # 解析价格折扣等信息
    def parsePrice(self,response):
        meta = response.meta
        data = json.loads(response.text).get('data')
        items = data.get('items')
        # shop = {}
        for i in items:
            thisId = i.get('id')
            if thisId == meta['SPU_NUM']:
                meta['SPU_Discount'] = i.get('price').get('sale_price').get('discount')  # TODO 折扣 这个算出来的？
                s = []
                for a in i.get('policy_list'):
                    if a.get('title'):
                        s.append(a.get('title'))
                meta['SPU_Service'] = s  # TODO 包邮……
                meta['SPU_Price'] = i.get('price').get('sale_price').get('price')
                meta['SPU_Price_Raw'] = i.get('price').get('origin_price')
                # meta['SPU_Coupon'] = ''
                # break
            for shop in meta['SPU_BUS_Other']:
                if shop['id']==thisId:
                    shop['price'] = i.get('price').get('sale_price').get('price')
                    break
            for sku in meta['skus']:
                if sku.get('pid') == thisId:
                    sku['price'] = i.get('price').get('sale_price').get('price')
                    break
        item2 = SKU()
        item2._values['SPU_NUM'] = meta['SPU_NUM']
        item2._values['SKU_TIT'] = meta['SPU_TIT']
        item2._values['SKU_PRICE'] = meta['skus']
        yield item2
        del meta['skus']
        item = XiaohongshuItem()
        item._values = meta
        yield item


