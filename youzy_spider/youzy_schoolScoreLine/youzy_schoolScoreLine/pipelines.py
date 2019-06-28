# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html


class YouzySchoolscorelinePipeline(object):
    def process_item(self, item, spider):
        return item

import datetime
import pymongo
from youzy_schoolScoreLine.items import SchoolScoreLineItem, MajorComparedDataItem, MajorScoreLineItem, Plan2019Item,ErrorSchoolItem

class MongoPipeline(object):
    def __init__(self, uri, db, post, tb1,tb2,tb3,tb4,tb5, auth=None):
        self.mongo_uri = uri
        self.mongo_db = db
        self.mongo_post = post
        self.tb1 = tb1
        self.tb2 = tb2
        self.tb3 = tb3
        self.tb4 = tb4
        self.tb5 = tb5
        self.db_auth = auth

    @classmethod
    def from_crawler(cls, crawler):
        return cls(
            uri=crawler.settings.get("MONGO_URI"),
            db=crawler.settings.get("MONGO_DB"),
            post=crawler.settings.get("MONGO_POST"),
            tb1=crawler.settings.get("MONGO_TB1"),
            tb2=crawler.settings.get("MONGO_TB2"),
            tb3=crawler.settings.get("MONGO_TB3"),
            tb4=crawler.settings.get("MONGO_TB4"),
            tb5=crawler.settings.get("MONGO_TB5"),
            auth=crawler.settings.get("DB_AUTH")
        )

    def open_spider(self, spider):
        self.client = pymongo.MongoClient("mongodb://{MONGO_HOST}:{MONGO_PORT}/".format(MONGO_HOST=self.mongo_uri, MONGO_PORT=self.mongo_post))
        if self.db_auth[0] != '':
            self.client.admin.authenticate(*self.db_auth)
        self.db = self.client[self.mongo_db]

    def process_item(self, item, spider):

        d = ['download_timeout', 'download_slot', 'depth', 'download_latency']
        postItem = dict(item)
        if postItem['school'] in spider.schoolList:
            spider.schoolList.remove(postItem['school'])
        postItem['getTime'] = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        for i in d:
            if i in postItem:
                del postItem[i]
        if isinstance(item,SchoolScoreLineItem):
            self.db[self.tb1].insert(postItem)
        elif isinstance(item,MajorComparedDataItem):
            self.db[self.tb2].insert(postItem)
        elif isinstance(item,MajorScoreLineItem):
            self.db[self.tb3].insert(postItem)
        elif isinstance(item,Plan2019Item):
            self.db[self.tb4].insert(postItem)
        return item

    def close_spider(self, spider):
        self.db[self.tb5].insert({"schoolList":spider.schoolList})
        self.client.close()
