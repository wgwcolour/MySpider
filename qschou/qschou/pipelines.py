# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import pymongo

class QschouPipeline(object):
    def process_item(self, item, spider):
        return item


class MongoPipeline(object):
    def __init__(self, uri, db, post, tb, auth=None):
        self.mongo_uri = uri
        self.mongo_db = db
        self.mongo_post = post
        self.tb = tb
        self.db_auth = auth

    @classmethod
    def from_crawler(cls, crawler):
        return cls(
            uri=crawler.settings.get("MONGO_URI"),
            db=crawler.settings.get("MONGO_DB"),
            post=crawler.settings.get("MONGO_POST"),
            tb=crawler.settings.get("MONGO_TB"),
            auth=crawler.settings.get("DB_AUTH")
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
        self.db[self.tb].insert(dict(item))
        return item

    def close_spider(self, spider):
        self.client.close()
