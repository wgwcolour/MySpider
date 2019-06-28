# -*- coding: utf-8 -*-
import scrapy
import json
import re
import requests
from ..items import QschouItem
import logging


class QingsongchouSpider(scrapy.Spider):
    name = 'qingsongchou'
    allowed_domains = ['yglian.qschou.com', 'partner-gateway.qschou.com']
    start_urls = ["https://partner-gateway.qschou.com/zghszjjh/index/tag/108/project?page=1",
                  "https://partner-gateway.qschou.com/zghszjjh/index/tag/109/project?page=1",
                  "https://partner-gateway.qschou.com/zgshfljjh/index/tag/131/project?page=1",
                  "https://partner-gateway.qschou.com/zhech/index/tag/103/project?page=1",
                  "https://partner-gateway.qschou.com/zhech/index/tag/104/project?page=1",
                  "https://partner-gateway.qschou.com/bjtsmm/index/tag/138/project?page=1"]

    # url_list = ["https://partner-gateway.qschou.com/zhech/index/tag/104/project?page=1"]
    # for i in url_list:
    #     respon = requests.get(i)
    #     next = json.loads(respon.text).get("data").get("next")
    #     if next:
    #         next_url = i.split("?page=")[0] + "?page=" + next
    #         start_urls.append(next_url)

    # logging.basicConfig(filename='example.log', filemode='w', level=logging.WARNING)

    def parse(self, response):
        js = json.loads(response.text)
        data = js.get("data")
        li = data.get("list")
        next = data.get("next")
        rule = re.compile("\.com/([a-zA-Z]+)/")
        ChannelId = re.findall(rule, response.url)[0]
        for i in li:
            project_no = i.get('project_no')
            meta = {}
            meta['Project_ID'] = project_no
            meta['Project_Intr_S'] = i.get('detail', '')
            Project_url = "https://yglian.qschou.com/gongyi/publicSite/detail?ChannelId={ChannelId}&id={project_no}".format(
                project_no=project_no, ChannelId=ChannelId)
            meta['Project_url'] = Project_url
            detail_url = "https://partner-gateway.qschou.com/{ChannelId}/project/{project_no}/info".format(
                project_no=project_no, ChannelId=ChannelId)
            yield scrapy.Request(url=detail_url, callback=self.parse_detail, meta=meta)
        #
        if next:
            next_url = response.url.split("?page=")[0] + "?page=" + next
            yield scrapy.Request(url=next_url, callback=self.parse)

    def parse_detail(self, response):
        js = json.loads(response.text)
        data = js.get("data")
        record_number = data.get("record_number", "")
        meta = response.meta
        meta['Project_recordnum'] = record_number
        meta['Project_TIT'] = data.get("title", '')
        meta['Project_LAB'] = data.get('tag_name', '')
        meta['Project_Domain'] = data.get('tag_name', '')  # 这个和项目标签是不是重复了？
        meta['Project_LAB_ID'] = data.get("tag_id", '')
        meta['Project_Top_ID'] = data.get("topic_id", '')
        meta['Project_Money'] = data.get('current_amount', '')
        meta['Project_Target'] = data.get('total_amount', '')
        meta['Project_Donate'] = data.get('backer_count', '')
        meta['Project_PCT'] = data.get('progress', '')
        meta['Feed_count'] = data.get('feed_count', '')
        meta['Backer_count'] = data.get("backer_count", '')
        meta['Follow_count'] = data.get("follow_count", '')
        meta['Share_count'] = data.get('share_count', '')
        meta['Front_cover'] = data.get("front_cover", '')
        meta['Follow_state'] = data.get("follow_state")
        meta['Project_Intr_date'] = data.get("created", '')
        detail = data.get('detail', '')
        meta['Project_Intr'] = detail
        rule1 = re.compile("src=\"(http.*?)\"", re.S)
        meta['Project_Intr_pic'] = re.findall(rule1, detail)
        meta['Launch_day'] = data.get('day', '')
        meta['Project_video'] = data.get("video_url", '')
        meta['Match_amount'] = data.get("match_amount", "")
        meta['Match_subject'] = data.get("match_subject", '')
        meta['Match_proportion'] = data.get("match_proportion", "")
        meta['Share_match_state'] = data.get("share_match_state")  # TODO
        meta['Share_match_amount'] = data.get('share_match_amount', '')
        meta['Match_count'] = data.get("match_count", '')
        meta['Match_id'] = data.get("match_id")
        meta['Total_digicash'] = data.get('total_digicash')
        meta['Active'] = data.get("active")
        meta['State'] = data.get("state")
        meta['Is_test'] = data.get("is_test")
        # meta['Execution_date'] =
        # https://partner-gateway.qschou.com/zghszjjh/project/201811150000000027822807/info
        # https://partner-gateway.qschou.com/zghszjjh/project/201811150000000027822807/feed
        url = response.url.replace("info", "feed")
        yield scrapy.Request(url=url, callback=self.parse_execution, meta=meta)

    def parse_execution(self, response):
        # https://partner-gateway.qschou.com/zghszjjh/project/201811150000000027822807/feed
        # https://partner-gateway.qschou.com/zghszjjh/project/201811150000000027822807/extra
        meta = response.meta
        meta["Execution"] = []
        data = json.loads(response.text).get('data')
        topics = data.get("topics", "")
        if topics:
            for i in topics:
                t = {}
                t['Execution_date'] = i.get("created")
                t['Execution_Plan_content'] = i.get("content")
                t['Execution_Plan_pic'] = []
                imgs = i.get("image")
                if imgs:
                    for img in imgs:
                        if img.get("thumb"):
                            t['Execution_Plan_pic'].append(img.get("thumb"))
                meta["Execution"].append(t)
        url = response.url.replace("feed", "extra")
        yield scrapy.Request(url=url, callback=self.parse_extra, meta=meta)

    def parse_extra(self, response):
        meta = response.meta
        data = json.loads(response.text).get('data')
        publish_organization = data.get("publish_organization")
        execution_organization = data.get("execution_organization")
        publisher = data.get("publisher")
        receive_fund = data.get("receive_fund")

        channel = publish_organization.get("channel")
        if channel:
            u = "https://partner-gateway.qschou.com/xadmin/site/prepare?channel=" + channel
            resp = requests.get(u)
            js_data = json.loads(resp.text).get("data", "")
            meta["NPO_LAU"] = js_data.get("name", "")
            meta["NPO_LAU_Logo"] = js_data.get("avatar", "")
            meta["NPO_LAU_Slogan"] = js_data.get("slogan", "")
            meta["NPO_LAU_Ptype"] = js_data.get("paid_type", "")
            meta["NPO_LAU_Pay"] = js_data.get("NPO_LAU_Pay", "")
        else:
            meta["NPO_LAU"] = ""
            meta["NPO_LAU_Logo"] = ""
            meta["NPO_LAU_Slogan"] = ""
            meta["NPO_LAU_Ptype"] = ""
            meta["NPO_LAU_Pay"] = ""
        # 发起机构
        meta['NPO_LAU_recodnum'] = publish_organization.get('social_credit_no', "")
        meta['NPO_LAU_Email'] = publish_organization.get("email", "")
        meta['NPO_LAU_TEL'] = publish_organization.get("phone", "")
        meta["NPO_LAU_Intro"] = publish_organization.get("intro", "")
        # 执行机构
        meta['NPO_EXE'] = execution_organization.get("name", "")
        meta['NPO_EXE_Logo'] = execution_organization.get("avatar", '')
        meta['NPO_EXE_Email'] = execution_organization.get("email", "")
        meta['NPO_EXE_TEL'] = execution_organization.get("phone", "")

        # TODO 下面这两个不知道有没有。找了好几个链接都没找到例子
        meta['NPO_EXE_Slogan'] = execution_organization.get('slogan', "")
        meta['NPO_EXE_recodnum'] = execution_organization.get("social_credit_no", "")

        # 发起人
        meta['P_LAU'] = publisher.get("name", "")
        meta['P_LAU_Logo'] = publisher.get("avatar", "")
        meta['P_LAU_Slogan'] = publisher.get("intro", "")  # 介绍
        meta['P_LAU_Email'] = publisher.get("email", "")
        meta['P_LAU_TEL'] = publisher.get("phone", "")

        # 善款接收方
        meta['NPO_REC'] = receive_fund.get("name", "")
        meta['NPO_REC_Bank'] = receive_fund.get("bank_location", '')
        meta['NPO_REC_card'] = receive_fund.get("bank_card_no", '')
        # TODO 下面这两个不知道有没有。也没找到例子
        meta['NPO_REC_Email'] = receive_fund.get("email", "")
        meta['NPO_REC_TEL'] = receive_fund.get('phone', "")
        meta['Donor'] = []
        # https://partner-gateway.qschou.com/zghszjjh/project/201811150000000027822807/extra
        # https://partner-gateway.qschou.com/zghszjjh/project/201809130000000021852210/backer?order_next_id=0&share_next_id=0
        url = response.url.replace("extra", "backer?order_next_id=0&share_next_id=0")
        yield scrapy.Request(url=url, callback=self.parse_Donor, meta=meta)

    def parse_Donor(self, response):
        meta = response.meta
        data = json.loads(response.text).get("data")
        li = data.get("list")
        meta['Project_Donor'] = data.get("count", "")
        if li:
            for i in li:
                info = {}
                user = i.get("user")
                info['Donor_ID'] = user.get("user_no", "")
                info['Donor_Name'] = user.get("nickname", '')
                info['Donor_Pic'] = user.get("avatar_thumb", '')
                info['Donor_Address'] = user.get("address", "")
                info['Donor_DA'] = i.get("pay_at", "")
                info['Donor_Money'] = i.get("money", "")
                info['Donor_Content'] = i.get("content")
                info['Donor_Match'] = i.get("match_amount", "")
                info['Donor_Rank'] = i.get("order_id", "")
                info['Backer_type'] = i.get("backer_type", "")
                info['Donor_Comment'] = i.get("comment", "")
                meta["Donor"].append(info)
        order_next_id = data.get("order_next_id", "")
        if order_next_id:
            url = response.url.split("order_next_id=")[0] + "order_next_id=" + str(order_next_id) + "&share_next_id=0"
            yield scrapy.Request(url=url, callback=self.parse_Donor, meta=meta)
        else:
            item = QschouItem()
            item._values = meta
            yield item
