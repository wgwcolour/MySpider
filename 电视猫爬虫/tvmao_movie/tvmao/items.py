# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class TvmaoItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    ID = scrapy.Field()
    Title = scrapy.Field()
    Role_info = scrapy.Field()
    Director = scrapy.Field()
    URL = scrapy.Field()
    Img = scrapy.Field()
    Viedo_rb = scrapy.Field()
    Screenwriter = scrapy.Field()
    Location = scrapy.Field()
    Intro_type = scrapy.Field()
    Intro_Era = scrapy.Field()
    Language = scrapy.Field()
    Intro_brief_des = scrapy.Field()
    PVNum = scrapy.Field()
    Score = scrapy.Field()
    W_watch = scrapy.Field()
    N_watch = scrapy.Field()
    review = scrapy.Field()
    Show_time = scrapy.Field()
    Relationship = scrapy.Field()

class ActorItem(scrapy.Item):
    Sub_id = scrapy.Field()
    Actor_id = scrapy.Field()
    Actor_name = scrapy.Field()
    Role_name = scrapy.Field()
    Role_intro = scrapy.Field()
    Actor_rating = scrapy.Field()
    Actor_url = scrapy.Field()

class subMainItem(scrapy.Item):
    Sub_main_id = scrapy.Field()
    Sub_id = scrapy.Field()
    Sub_info_num = scrapy.Field()
    Sub_info_title = scrapy.Field()
    Sub_info_pic = scrapy.Field()
    Sub_info_detail_txt = scrapy.Field()
    Sub_publishTime = scrapy.Field()
    Sub_review = scrapy.Field()


