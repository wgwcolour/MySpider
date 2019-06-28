# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import pymongo
from scrapy.conf import settings
from jdWare.items import SpuItem
from jdWare.items import SkuItem
from jdWare.items import ReviewItem
import datetime
class JdwarePipeline(object):

	def __init__(self):
		self.client = pymongo.MongoClient(host = settings['MONGO_HOST'], port = settings['MONGO_PORT'])
		self.db = self.client[settings['MONGO_DB']]

	def process_item(self, item, spider):
		item._values['Platform']='京东'
		item._values['Date']=datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
		postItem = dict(item)
		d = ['download_timeout','download_slot','depth','download_latency']
		for i in d:
			if i in postItem:
				del postItem[i]
		if isinstance(item, SpuItem):

			self.db["SPU"].insert(postItem)
		elif isinstance(item, SkuItem):
			self.db["SKU"].insert(postItem)
		elif isinstance(item, ReviewItem):
			self.db["REVIEW"].insert(postItem)