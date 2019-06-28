# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html


class TvmaoPipeline(object):
    def process_item(self, item, spider):
        return item

import pymongo
class MongoPipeline(object):
    def __init__(self, uri, db, post, tb,tb1,tb2, auth=None):
        self.mongo_uri = uri
        self.mongo_db = db
        self.mongo_post = post
        self.tb = tb
        self.tb1 = tb1
        self.tb2 = tb2
        self.db_auth = auth

    @classmethod
    def from_crawler(cls, crawler):
        return cls(
            uri=crawler.settings.get("MONGO_URI"),
            db=crawler.settings.get("MONGO_DB"),
            post=crawler.settings.get("MONGO_POST"),
            tb=crawler.settings.get("MONGO_TB"),
            tb1 = crawler.settings.get("MONGO_TB1"),
            tb2 = crawler.settings.get("MONGO_TB2"),
            auth=crawler.settings.get("DB_AUTH") if crawler.settings.get("DB_AUTH")[0] and crawler.settings.get("DB_AUTH")[1] else None

        )

    def open_spider(self, spider):
        self.client = pymongo.MongoClient(self.mongo_uri)
        if self.db_auth:
            self.db = self.client[self.mongo_db]
            self.db.authenticate(*self.db_auth)
        # self.Client = self.client[self.mongo_db]
        else:
            self.db = self.client[self.mongo_db]

    def process_item(self, item, spider):
        if item._values.get("ID") is not None:
            self.db[self.tb].insert(dict(item))
        elif item._values.get("Actor_id") is not None:
            self.db[self.tb1].insert(dict(item))
        else:
            self.db[self.tb2].insert(dict(item))
        return item

    def close_spider(self, spider):
        self.client.close()
