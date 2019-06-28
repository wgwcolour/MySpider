# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html


class XiaohongshuPipeline(object):
    def process_item(self, item, spider):
        return item
from xiaohongshu.items import XiaohongshuItem,Review,SKU

import pymongo


class MongoPipeline(object):
    def __init__(self, uri, db, post, tb1,tb2,tb3, auth=None):
        self.mongo_uri = uri
        self.mongo_db = db
        self.mongo_post = post
        self.tb1 = tb1
        self.tb2 = tb2
        self.tb3 = tb3
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
            auth=crawler.settings.get("DB_AUTH")
        )

    def open_spider(self, spider):
        self.client = pymongo.MongoClient(self.mongo_uri)
        if self.db_auth[0] != '':
            self.db = self.client[self.mongo_db]
            self.db.authenticate(*self.db_auth)
        # self.Client = self.client[self.mongo_db]
        else:
            self.db = self.client[self.mongo_db]

    def process_item(self, item, spider):
        d = ['download_timeout', 'download_slot', 'depth', 'download_latency']
        postItem = dict(item)
        for i in d:
            if i in postItem:
                del postItem[i]
        if isinstance(item,XiaohongshuItem):
            self.db[self.tb1].insert(postItem)
        elif isinstance(item,Review):
            self.db[self.tb2].insert(postItem)
        elif isinstance(item,SKU):
            self.db[self.tb3].insert(postItem)
        return item

    def close_spider(self, spider):
        self.client.close()
