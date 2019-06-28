# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class SpuItem(scrapy.Item):
	SPU_NUM  = scrapy.Field()
	Category_L1  = scrapy.Field()
	# SPU_ID   = scrapy.Field()
	SPU_URL  = scrapy.Field()
	SPU_TIT  = scrapy.Field()
	SPU_PIC  = scrapy.Field()
	SPU_Price  = scrapy.Field()
	SPU_Price_Raw  = scrapy.Field()
	SPU_Review  = scrapy.Field()
	SPU_Score  = scrapy.Field()
	SPU_Score_ALL  = scrapy.Field()
	SPU_DES  = scrapy.Field()
	SPU_SPEC = scrapy.Field()
	SPU_Product_PIC = scrapy.Field()
	Platform = scrapy.Field()
	Date = scrapy.Field()
	Category_L2 = scrapy.Field()
	Total_Rank = scrapy.Field()
	Sale_Rank = scrapy.Field()
	New_Rank = scrapy.Field()
	Liking_Rank = scrapy.Field()
	WOM_Rank = scrapy.Field()
	Price_Rank = scrapy.Field()
	SPU_LAB = scrapy.Field()
	SPU_Sale_Month = scrapy.Field()
	SPU_huabei = scrapy.Field()
	SPU_Inventory = scrapy.Field()
	SPU_POP = scrapy.Field()
	SPU_Service = scrapy.Field()
	SPU_Coupon = scrapy.Field()



class SkuItem(scrapy.Item):
	SPU_NUM  = scrapy.Field()
	SKU_TIT  = scrapy.Field()
	SKU_PRICE = scrapy.Field()
	remark = scrapy.Field()
	Platform = scrapy.Field()
	Date = scrapy.Field()



class ReviewItem(scrapy.Item):
	SPU_NUM = scrapy.Field()
	SPU_TIT = scrapy.Field()
	U_NAME = scrapy.Field()
	U_LEVEL = scrapy.Field()
	SKU_TIT = scrapy.Field()
	REV_TIME = scrapy.Field()
	REV_CONTENT = scrapy.Field()
	REV_SCORE = scrapy.Field()
	REV_PIC = scrapy.Field()
	Platform=scrapy.Field()
	Date=scrapy.Field()
