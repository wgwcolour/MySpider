# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class ImdbItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    ID = scrapy.Field()
    Title = scrapy.Field()
    Role_info = scrapy.Field()
    Director = scrapy.Field()
    URL = scrapy.Field()
    Img = scrapy.Field()
    Viedo_rb = scrapy.Field()
    Intro_type = scrapy.Field()
    Intro_Era = scrapy.Field()
    Intro_brief_des = scrapy.Field()
    PVNum = scrapy.Field()
    Score = scrapy.Field()
    Metascore = scrapy.Field()
    RevUser = scrapy.Field()
    RevCritic = scrapy.Field()
    Popularity = scrapy.Field()

    PProduce = scrapy.Field()
    PMusic = scrapy.Field()
    PCine = scrapy.Field()
    PEditing = scrapy.Field()
    PCasting = scrapy.Field()
    PPDesign = scrapy.Field()
    PArtDir = scrapy.Field()
    PDecoration = scrapy.Field()
    PCDesign = scrapy.Field()
    PMakeup = scrapy.Field()
    PSDirector = scrapy.Field()
    PArtDep = scrapy.Field()
    PSoundDep = scrapy.Field()
    PSpecialEff = scrapy.Field()
    PVisualEff = scrapy.Field()
    PStunts = scrapy.Field()
    PCameraDep = scrapy.Field()
    PCastingDep = scrapy.Field()
    PCostumeDep = scrapy.Field()
    PEditorialDep = scrapy.Field()
    PLocationMan = scrapy.Field()
    PMusicDep = scrapy.Field()
    PTransportationDep = scrapy.Field()
    POther = scrapy.Field()
    PThanks = scrapy.Field()
    Summaries = scrapy.Field()
    Synopsis = scrapy.Field()
    PlotKeywords = scrapy.Field()
    Taglines = scrapy.Field()
    Genres = scrapy.Field()
    Off_sites = scrapy.Field()
    Country = scrapy.Field()
    Language = scrapy.Field()
    Release_date = scrapy.Field()
    Budget = scrapy.Field()
    Open_weekend = scrapy.Field()
    Gross = scrapy.Field()
    W_Gross = scrapy.Field()
    Runtime = scrapy.Field()
    SoundMix = scrapy.Field()
    Color = scrapy.Field()
    Aspect_ratio = scrapy.Field()

class ImdbItemActor(scrapy.Item):
    Sub_id = scrapy.Field()
    Actor_id = scrapy.Field()
    Actor_name = scrapy.Field()
    Role_name = scrapy.Field()
    Actor_Influence = scrapy.Field()
    Actor_avatar = scrapy.Field()
    Actor_career = scrapy.Field()
    Actor_birthday = scrapy.Field()
    Actor_infor = scrapy.Field()

class Awards(scrapy.Item):
    Sub_id = scrapy.Field()
    awards = scrapy.Field()