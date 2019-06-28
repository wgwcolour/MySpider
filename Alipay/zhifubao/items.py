# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class ZhifubaoItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    Project_ID = scrapy.Field()  # 项目id
    Project_recordnum = scrapy.Field()  # 民政部备案号
    Project_url = scrapy.Field()  # 项目url
    Project_TIT = scrapy.Field()  # 标题
    Project_Intr_S = scrapy.Field()  # 简介
    Project_Money = scrapy.Field()  # 已筹金额
    Project_Target = scrapy.Field()  # 目标金额
    Project_Donor = scrapy.Field()  # 捐款人数
    Project_NGO = scrapy.Field()  # 发起机构
    Project_PCT = scrapy.Field()  # 完成度
    Project_Date = scrapy.Field()  # 项目时间
    Project_Domain = scrapy.Field()  # 所属领域
    Front_cover = scrapy.Field()  # 首页图片
    Project_Intr_date = scrapy.Field()  # 故事时间
    Project_Intr = scrapy.Field()  # 故事内容
    Project_Intr_pic = scrapy.Field()  # 故事图片
    Execution = scrapy.Field() # 进展追溯
    # Execution_date = scrapy.Field()  # 追溯时间
    # Execution_Plan = scrapy.Field()  # 追溯内容
    # Execution_Plan_pic = scrapy.Field()  # 追溯图片

