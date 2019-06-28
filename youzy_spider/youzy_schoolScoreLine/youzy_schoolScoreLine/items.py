# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class SchoolScoreLineItem(scrapy.Item):
    # define the fields for your item here like:
    gid = scrapy.Field()                # 全局id：省份id+文理+uCodeNum
    provinceId = scrapy.Field()         # 省份id
    course = scrapy.Field()             # 文理科：0理科，1文科
    schoolId = scrapy.Field()           # 优志愿学校id
    school = scrapy.Field()             # 优志愿学校名称
    provinceName = scrapy.Field()       # 省份名称
    uCodeNum = scrapy.Field()           # UCodeNum
    admissCode = scrapy.Field()         # 招生代码
    collegeId = scrapy.Field()          # 优志愿学校id
    collegeName = scrapy.Field()        # 招生名称
    sort = scrapy.Field()               # 未知作用排序码
    isOld = scrapy.Field()              # 未知
    codeChangeYear = scrapy.Field()     # 未知
    id = scrapy.Field()                 # 未知
    schoolSortNo = scrapy.Field()       # 页面上的学校排序码
    result = scrapy.Field()             # 接口返回的json数据
    getTime = scrapy.Field()            # 采集时间

class MajorComparedDataItem(scrapy.Item):
    gid = scrapy.Field()
    provinceId = scrapy.Field()
    course = scrapy.Field()
    schoolId = scrapy.Field()
    school = scrapy.Field()
    provinceName = scrapy.Field()
    uCodeNum = scrapy.Field()
    batch = scrapy.Field()              # 批次id
    batchName = scrapy.Field()          # 批次名称
    admissCode = scrapy.Field()
    collegeId = scrapy.Field()
    collegeName = scrapy.Field()
    sort = scrapy.Field()
    isOld = scrapy.Field()
    codeChangeYear = scrapy.Field()
    id = scrapy.Field()
    schoolSortNo = scrapy.Field()
    result = scrapy.Field()
    getTime = scrapy.Field()

class MajorScoreLineItem(scrapy.Item):
    gid = scrapy.Field()
    provinceId = scrapy.Field()
    course = scrapy.Field()
    schoolId = scrapy.Field()
    school = scrapy.Field()
    provinceName = scrapy.Field()
    uCodeNum = scrapy.Field()
    admissCode = scrapy.Field()
    collegeId = scrapy.Field()
    collegeName = scrapy.Field()
    sort = scrapy.Field()
    isOld = scrapy.Field()
    codeChangeYear = scrapy.Field()
    id = scrapy.Field()
    schoolSortNo = scrapy.Field()
    result = scrapy.Field()
    getTime = scrapy.Field()

class Plan2019Item(scrapy.Item):
    gid = scrapy.Field()
    provinceId = scrapy.Field()
    course = scrapy.Field()
    schoolId = scrapy.Field()
    school = scrapy.Field()
    provinceName = scrapy.Field()
    uCodeNum = scrapy.Field()
    admissCode = scrapy.Field()
    collegeId = scrapy.Field()
    collegeName = scrapy.Field()
    sort = scrapy.Field()
    isOld = scrapy.Field()
    codeChangeYear = scrapy.Field()
    id = scrapy.Field()
    schoolSortNo = scrapy.Field()
    result = scrapy.Field()
    getTime = scrapy.Field()

class ErrorSchoolItem(scrapy.Item):
    schoolList = scrapy.Field()
    getTime = scrapy.Field()