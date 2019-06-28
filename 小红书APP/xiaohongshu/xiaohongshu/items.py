# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class XiaohongshuItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    Category_L1 = scrapy.Field()
    Category_L2 = scrapy.Field()
    Sale_Rank = scrapy.Field()
    Liking = scrapy.Field()
    SPU_NUM = scrapy.Field()
    SPU_URL = scrapy.Field()
    SPU_TIT = scrapy.Field()
    SPU_PIC = scrapy.Field()
    SPU_Brand = scrapy.Field()
    SPU_Brand_GEO = scrapy.Field()
    SPU_Price = scrapy.Field()
    SPU_Price_Raw = scrapy.Field()
    SPU_Discount = scrapy.Field()
    SPU_Service = scrapy.Field()
    SPU_Coupon = scrapy.Field()
    SPU_DES = scrapy.Field()
    SPU_SPEC = scrapy.Field()
    SPU_Product_PIC = scrapy.Field()
    SPU_BUS = scrapy.Field()
    SPU_BUS_Other = scrapy.Field()

class Review(scrapy.Item):
    SPU_NUM = scrapy.Field()
    U_NAME = scrapy.Field()
    U_LEVEL = scrapy.Field()
    Favorites = scrapy.Field()
    Thumb_up = scrapy.Field()
    SKU_TIT = scrapy.Field()
    REV_CONTENT = scrapy.Field()
    REV_PIC = scrapy.Field()

class SKU(scrapy.Item):
    SPU_NUM = scrapy.Field()
    SKU_TIT = scrapy.Field()
    SKU_PRICE = scrapy.Field()