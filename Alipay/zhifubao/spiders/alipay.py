# -*- coding: utf-8 -*-
import scrapy

from ..items import ZhifubaoItem
import re
import time
import json
import requests
import logging


class AlipaySpider(scrapy.Spider):
    # logging.basicConfig(filename='example.log', filemode='w', level=logging.WARNING)
    name = 'alipay'
    allowed_domains = ['love.alipay.com']
    start_urls = []
    u = "https://love.alipay.com/donate/itemList.htm?page=1&&donateType=&itemClassified=&orderType=gmt_create_desc&donateShowName="
    response1 = requests.get(u)
    _rule = re.compile("class=\"ui-page-goto\".*?<span>(\d+)</",re.S)
    pages = re.findall(_rule,response1.text)[2]
    for i in range(int(pages)):
        start_urls.append("https://love.alipay.com/donate/itemList.htm?page=" + str(i + 1) + "&&donateType=&itemClassified=&orderType=gmt_create_desc&donateShowName=")

    def parse(self, response):
        li = response.xpath("//li[@class='donate-item-default-li fn-clear']")
        for selector in li:
            url = selector.xpath(".//a[@class='donate-item-default-pic-a']/@href").extract_first()
            summary = selector.xpath(".//dd[@class='donate-item-default-desc']/text()").extract_first()
            ft_bold = selector.xpath(".//em[@class='ft-orange ft-bold']/text()").extract_first()
            span = selector.xpath(".//span[@class='donate-info-amount-left']/text()").extract_first()  # 筹款目标，有的没有筹款目标
            dt = selector.xpath(".//dt[@class='donate-item-default-title']/span/text()").extract_first()[1:-1]
            ruler = re.compile("donate-item-default-dd\">发\s+布\s+人：(.*?)</")
            postuser = re.findall(ruler, response.text)[0]
            meta = {"summary": summary, "ft_bold": ft_bold, "span": span, "dt": dt, "postuser": postuser}
            yield scrapy.Request(url=url, callback=self.parse_data, meta=meta)
        # rule = re.compile("page=(\d+)&")
        # page = re.findall(rule, response.url)[0]
        # next_url = response.xpath("//a[@class='sl-rc-wrap ui-page-turn']/@href").extract_first()
        # n_page = re.findall(rule, next_url)[0]
        # if int(n_page) > int(page):
        #     yield scrapy.Request(url=next_url, callback=self.parse)

    def parse_data(self, response):
        # item = ZhifubaoItem()
        meta = {}
        # url = scrapy.Request()._get_url()
        # html = response.xpath()
        meta['Project_ID'] = response.url.split('name=')[1]  # 项目id
        ruler = re.compile("募捐方案备案编号：([0-9a-zA-Z]+)", re.S)
        code = re.findall(ruler, response.text)
        if not code:
            ruler = re.compile("公开募捐活动备案编号：([0-9a-zA-Z]+)", re.S)
            code = re.findall(ruler, response.text)
        if code:
            meta['Project_recordnum'] = code[0]  # 民政部备案号
        else:
            meta['Project_recordnum'] = ''  # 民政部备案号

        meta['Project_url'] = response.url  # 项目url
        meta['Project_TIT'] = response.xpath("//h2[@class='fn-left donate-detail-title']/text()").extract_first()  # 标题
        meta['Project_Intr_S'] = response.meta['summary'].replace("\n", '').replace("\t", '')  # 简介
        meta['Project_Money'] = response.meta['ft_bold']  # 已筹金额
        meta['Project_Target'] = response.meta['span']  # 目标金额
        ruler1 = re.compile("参捐人数：.*?>(\d+)<", re.S)
        meta['Project_Donor'] = re.findall(ruler1, response.text)[0]  # 捐款人数
        meta['Project_NGO'] = response.meta['postuser']
        # meta['Project_NGO'] = \
        # response.xpath("//div[@class='donate-list-info-puborg-text']/text()").extract_first().split("：")[1]  # 发起机构
        meta['Project_PCT'] = response.xpath("//div[@class='ui-progressbar-s']/span/text()").extract_first()  # 完成度
        ruler3 = re.compile("项目时间：(.*?)</", re.S)
        meta['Project_Date'] = re.findall(ruler3, response.text)[0]  # 项目时间
        meta['Project_Domain'] = response.meta['dt']  # 所属领域
        ruler4 = re.compile("lazyload-src=\"(.*?)\"", re.S)
        meta['Front_cover'] = re.findall(ruler4, response.text)[0]  # 首页图片
        # meta['Project_Intr_date'] = ''  # 故事时间
        ruler5 = re.compile("\.html\('(.*?)'\);", re.S)
        content = re.findall(ruler5, response.text)[0]
        meta['Project_Intr'] = content  # 故事内容
        ruler6 = re.compile("src=&quot;(https:.*?image.*?)\s", re.S)
        meta['Project_Intr_pic'] = re.findall(ruler6, content)  # 故事图片
        meta['Execution'] = []
        t = str(round(time.time() * 1000))
        if response.url.find("&") == -1:
            json_url = "https://love.alipay.com/donate/showFeedBack.json?name=" + response.url.split('name=')[1] + "&page=1&t=" + t + "&_input_charset=utf-8"
        else:
            rr = re.compile("name=(.*?)&")
            id = re.findall(rr,response.url)[0]
            json_url = "https://love.alipay.com/donate/showFeedBack.json?name=" + id + "&page=1&t=" + t + "&_input_charset=utf-8"
        yield scrapy.Request(url=json_url, callback=self.json_parse, meta=meta)

    def json_parse(self, response):
        obj_json = json.loads(response.text)
        item = ZhifubaoItem()
        meta = response.meta
        if obj_json.get("stat") == "ok":
            donateFeedbackPageModelList = obj_json.get("donateFeedbackPageModelList")
            for i in donateFeedbackPageModelList:
                obj = {}
                obj['Execution_Plan_pic'] = []
                bigPicPathList = i.get('bigPicPathList')
                if bigPicPathList:
                    for pic in bigPicPathList:
                        picViewUrl = pic.get("picViewUrl")
                        obj['Execution_Plan_pic'].append(picViewUrl)

                donateFeedbackProgressModel = i.get("donateFeedbackProgressModel")
                obj['Execution_Plan_content'] = donateFeedbackProgressModel.get("feedback")
                obj['Execution_date'] = donateFeedbackProgressModel.get("gmtAuditStr")
                meta['Execution'].append(obj)

            nextPage = obj_json.get('paginator').get('nextPage')
            lastPage = obj_json.get('paginator').get('lastPage')
            page = obj_json.get('paginator').get('page')
            if page == lastPage:  # 到了最后一页了
                item._values = meta
                # item.fields = meta
                yield item
            else:
                t = str(round(time.time() * 1000))
                url = response.url.split("page=")[0] + "page=" + str(nextPage) + "&t=" + t + "&_input_charset=utf-8"
                yield scrapy.Request(url=url, callback=self.json_parse, meta=meta)
            # item['Execution_date'] = ''  # 追溯时间
            # item['Execution_Plan_content'] = ''  # 追溯内容
            # item['Execution_Plan_pic'] = ''  # 追溯图片
        else:
            item._values = meta
            yield item
